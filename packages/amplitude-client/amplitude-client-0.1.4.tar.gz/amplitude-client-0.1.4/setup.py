# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amplitude_client', 'amplitude_client.resources']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-client-manager>=1.1.1,<2.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'aioresponses>=0.6.4,<0.7.0',
 'json-schema-env-validator>=1.0.5,<2.0.0',
 'jsonschema>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'amplitude-client',
    'version': '0.1.4',
    'description': 'A simple aiohttp based python client for Amplitude',
    'long_description': None,
    'author': 'Ismael Alaoui',
    'author_email': 'ismael@onna.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
