# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pippi_trigger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pippi-trigger',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Edward George',
    'author_email': 'edward.george@maersk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
