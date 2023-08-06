# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ca_bundle']
setup_kwargs = {
    'name': 'ca-bundle',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Matúš Ferech',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
