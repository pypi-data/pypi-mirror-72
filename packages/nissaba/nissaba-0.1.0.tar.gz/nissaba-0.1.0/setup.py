# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nissaba']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nissaba',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sam Broster',
    'author_email': 'sam@broster.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
