# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlcon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sqlcon',
    'version': '0.1.2',
    'description': 'Construct indented SQL from Python.',
    'long_description': None,
    'author': 'Timothy Corbett-Clark',
    'author_email': 'timothy.corbettclark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
