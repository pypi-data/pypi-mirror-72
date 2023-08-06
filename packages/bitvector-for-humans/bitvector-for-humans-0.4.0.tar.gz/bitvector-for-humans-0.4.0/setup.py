# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitvector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bitvector-for-humans',
    'version': '0.4.0',
    'description': 'A simple bit vector class for Humans™.',
    'long_description': None,
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
