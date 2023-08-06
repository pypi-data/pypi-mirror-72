import asyncio
import json
from inspect import isawaitable
from typing import Any, AsyncGenerator, Callable, Dict, List, Union, Optional, cast

import graphene
from graphql import ExecutionResult, GraphQLError, Middleware, format_error
from starlette.datastructures import UploadFile
from starlette.requests import Request, HTTPConnection
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

GQL_CONNECTION_ACK = "connection_ack"
GQL_CONNECTION_ERROR = "connection_error"
GQL_CONNECTION_INIT = "connection_init"
GQL_CONNECTION_TERMINATE = "connection_terminate"
GQL_COMPLETE = "complete"
GQL_DATA = "data"
GQL_ERROR = "error"
GQL_START = "start"
GQL_STOP = "stop"

ContextValue = Union[Any, Callable[[Any], Any]]
RootValue = Any


class GraphQLApp:
    def __init__(
        self,
        schema: graphene.Schema,
        playground: bool = True,
        context_value: ContextValue = None,
        root_value: RootValue = None,
        middleware: Optional[Middleware] = None,
    ):
        self.schema = schema
        self.playground = playground
        self.context_value = context_value
        self.root_value = root_value
        self.middleware = middleware

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope=scope, receive=receive)
            response: Response
            if request.method == "GET" and self.playground:
                response = HTMLResponse(PLAYGROUND_HTML)
            elif request.method == "POST":
                response = await self._handle_http_request(request)
            else:
                response = Response(status_code=405)
            await response(scope, receive, send)
        elif scope["type"] == "websocket":
            websocket = WebSocket(scope=scope, receive=receive, send=send)
            await self._run_websocket_server(websocket)
        else:
            raise ValueError(f"Unsupported scope type: ${scope['type']}")

    async def _get_context_value(self, request: HTTPConnection) -> Any:
        if callable(self.context_value):
            context = self.context_value(request)
            if isawaitable(context):
                context = await context
            return context
        else:
            return self.context_value or {"request": request}

    async def _handle_http_request(self, request: Request) -> Response:
        try:
            operations = await _get_operation_from_request(request)
        except ValueError as error:
            return JSONResponse({"errors": [error.args[0]]}, status_code=400)

        if isinstance(operations, list):
            return JSONResponse({"errors": ["This server does not support batching"]}, status_code=400)
        else:
            operation = operations

        query = operation["query"]
        variable_values = operation.get("variables")
        operation_name = operation.get("operationName")
        context_value = await self._get_context_value(request)

        result = await self.schema.execute_async(
            source=query,
            context_value=context_value,
            root_value=self.root_value,
            middleware=self.middleware,
            variable_values=variable_values,
            operation_name=operation_name,
        )

        response = {"data": result.data}
        if result.errors:
            response["errors"] = [format_error(error) for error in result.errors]

        status_code = 200 if not result.errors else 400
        return JSONResponse(response, status_code=status_code)

    async def _run_websocket_server(self, websocket: WebSocket) -> None:
        subscriptions: Dict[str, AsyncGenerator] = {}
        await websocket.accept("graphql-ws")
        try:
            while (
                websocket.client_state != WebSocketState.DISCONNECTED
                and websocket.application_state != WebSocketState.DISCONNECTED
            ):
                message = await websocket.receive_json()
                await self._handle_websocket_message(message, websocket, subscriptions)
        except WebSocketDisconnect:
            pass
        finally:
            for operation_id in subscriptions:
                await subscriptions[operation_id].aclose()

    async def _handle_websocket_message(
        self,
        message: dict,
        websocket: WebSocket,
        subscriptions: Dict[str, AsyncGenerator],
    ):
        operation_id = cast(str, message.get("id"))
        message_type = cast(str, message.get("type"))

        if message_type == GQL_CONNECTION_INIT:
            await websocket.send_json({"type": GQL_CONNECTION_ACK})
        elif message_type == GQL_CONNECTION_TERMINATE:
            await websocket.close()
        elif message_type == GQL_START:
            await self._start_subscription(
                message.get("payload"), operation_id, websocket, subscriptions
            )
        elif message_type == GQL_STOP:
            if operation_id in subscriptions:
                await subscriptions[operation_id].aclose()
                del subscriptions[operation_id]

    async def _start_subscription(
        self,
        data: Any,
        operation_id: str,
        websocket: WebSocket,
        subscriptions: Dict[str, AsyncGenerator],
    ):
        query = data["query"]
        variable_values = data.get("variables")
        operation_name = data.get("operationName")
        context_value = await self._get_context_value(websocket)

        errors: List[GraphQLError] = []
        try:
            result = await self.schema.subscribe(
                query,
                context_value=context_value,
                root_value=self.root_value,
                variable_values=variable_values,
                operation_name=operation_name,
            )
            if isinstance(result, ExecutionResult) and result.errors:
                errors = result.errors
        except GraphQLError as e:
            errors = [e]

        if errors:
            results = [format_error(error) for error in errors]
            await websocket.send_json(
                {"type": GQL_ERROR, "id": operation_id, "payload": results[0]}
            )
        else:
            asyncgen = cast(AsyncGenerator, result)
            subscriptions[operation_id] = asyncgen
            asyncio.ensure_future(
                self._observe_subscription(asyncgen, operation_id, websocket)
            )

    async def _observe_subscription(
        self, asyncgen: AsyncGenerator, operation_id: str, websocket: WebSocket
    ) -> None:
        try:
            async for result in asyncgen:
                payload = {}
                if result.data:
                    payload["data"] = result.data
                if result.errors:
                    payload["errors"] = [format_error(error) for error in result.errors]
                await websocket.send_json(
                    {"type": GQL_DATA, "id": operation_id, "payload": payload}
                )
        except Exception as error:
            if not isinstance(error, GraphQLError):
                error = GraphQLError(str(error), original_error=error)
            await websocket.send_json(
                {
                    "type": GQL_DATA,
                    "id": operation_id,
                    "payload": {"errors": [format_error(error)]},
                }
            )

        if (
            websocket.client_state != WebSocketState.DISCONNECTED
            and websocket.application_state != WebSocketState.DISCONNECTED
        ):
            await websocket.send_json({"type": GQL_COMPLETE, "id": operation_id})


async def _get_operation_from_request(request: Request):
    content_type = request.headers.get("Content-Type", "").split(";")[0]
    if content_type == "application/json":
        try:
            return await request.json()
        except (TypeError, ValueError):
            raise ValueError("Request body is not a valid JSON")
    elif content_type == "multipart/form-data":
        return await _get_operation_from_multipart(request)
    else:
        raise ValueError("Content-type must be application/json or multipart/form-data")


async def _get_operation_from_multipart(request: Request):
    try:
        request_body = await request.form()
    except ValueError:
        raise ValueError("Request body is not a valid multipart/form-data")

    try:
        operations = json.loads(request_body.get("operations"))
    except (TypeError, ValueError):
        raise ValueError("'operations' must be a valid JSON")
    if not isinstance(operations, (dict, list)):
        raise ValueError("'operations' field must be an Object or an Array")

    try:
        name_path_map = json.loads(request_body.get("map"))
    except (TypeError, ValueError):
        raise ValueError("'map' field must be a valid JSON")
    if not isinstance(name_path_map, dict):
        raise ValueError("'map' field must be an Object")

    files = {k: v for (k, v) in request_body.items() if isinstance(v, UploadFile)}
    for (name, paths) in name_path_map.items():
        for path in paths:
            path = tuple(path.split("."))
            _inject_file_to_operations(operations, files[name], path)

    return operations


def _inject_file_to_operations(ops_tree, _file, path):
    key = path[0]
    try:
        key = int(key)
    except ValueError:
        pass
    if len(path) == 1:
        if ops_tree[key] is None:
            ops_tree[key] = _file
    else:
        _inject_file_to_operations(ops_tree[key], _file, path[1:])


PLAYGROUND_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset=utf-8/>
  <meta name="viewport" content="user-scalable=no, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, minimal-ui">
  <title>GraphQL Playground</title>
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
  <link rel="shortcut icon" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/favicon.png" />
  <script src="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
</head>
<body>
  <div id="root">
    <style>
      body {
        background-color: rgb(23, 42, 58);
        font-family: Open Sans, sans-serif;
        height: 90vh;
      }
      #root {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .loading {
        font-size: 32px;
        font-weight: 200;
        color: rgba(255, 255, 255, .6);
        margin-left: 20px;
      }
      img {
        width: 78px;
        height: 78px;
      }
      .title {
        font-weight: 400;
      }
    </style>
    <img src='//cdn.jsdelivr.net/npm/graphql-playground-react/build/logo.png' alt=''>
    <div class="loading"> Loading
      <span class="title">GraphQL Playground</span>
    </div>
  </div>
  <script>window.addEventListener('load', function (event) {
      GraphQLPlayground.init(document.getElementById('root'), {
        // options as 'endpoint' belong here
      })
    })</script>
</body>
</html>
""".strip()
