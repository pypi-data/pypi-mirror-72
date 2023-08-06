# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nissaba']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nissaba',
    'version': '0.2.0',
    'description': 'A utiltiy for managing test results',
    'long_description': None,
    'author': 'Samuel Broster',
    'author_email': 's.h.broster+pypi@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shbroster/nissaba',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
