# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pbwrap']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0',
 'requests>=2.23,<3.0',
 'twine>=3.1,<4.0',
 'wheel>=0.34.2,<0.35.0']

setup_kwargs = {
    'name': 'pbwrap',
    'version': '1.2.1',
    'description': 'Pastebin API Wrapper',
    'long_description': None,
    'author': 'Mikts',
    'author_email': 'mikts94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
