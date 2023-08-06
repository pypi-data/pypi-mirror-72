# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['range_digit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'range-digit',
    'version': '0.0.3',
    'description': '',
    'long_description': "## description\n\n`range-digit` is library of decimal digit which has `low` and `sup`.\n\n```\nd = RangeDigit('1.240')\nprint(d)  # 1.240\nprint(d - Decimal(1.2))  # 0.040\nprint(d / 2)  # 0.620\nprint(d.low)  # 1.2395\nprint(d.sup)  # 1.2405\nprint(d.tostr())  # <RangeDigit [1.2395 - 1.2405)>\n```",
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
