# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doveseed']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1,<2.0',
 'jinja2>=2.10,<3.0',
 'tinydb>=3.15,<4.0',
 'typing_extensions>=3.7,<4.0']

setup_kwargs = {
    'name': 'doveseed',
    'version': '1.0.0',
    'description': 'Doveseed is a backend service for email subscriptions to RSS feeds.',
    'long_description': None,
    'author': 'Jan Gosmann',
    'author_email': 'jan@hyper-world.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
