# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['range_digit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'range-digit',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/range-digit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
