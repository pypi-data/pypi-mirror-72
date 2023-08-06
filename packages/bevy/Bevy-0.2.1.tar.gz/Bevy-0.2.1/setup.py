# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bevy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bevy',
    'version': '0.2.1',
    'description': 'Simple app framework that helps you build looesly coupled applications.',
    'long_description': None,
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
