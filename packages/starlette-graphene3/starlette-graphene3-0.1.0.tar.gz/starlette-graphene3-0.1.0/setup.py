# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['starlette_graphene3']
install_requires = \
['graphene>=3.0b', 'starlette>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'starlette-graphene3',
    'version': '0.1.0',
    'description': 'Use Graphene v3 on Starlette',
    'long_description': None,
    'author': 'Taku Fukada',
    'author_email': 'naninunenor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
