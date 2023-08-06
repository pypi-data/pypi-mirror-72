# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['topdown']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'topdown',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Kevin Schiroo',
    'author_email': 'kjschiroo@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
