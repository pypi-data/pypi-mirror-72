# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yatb']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.13.3,<0.14.0', 'pydantic>=1.5.1,<2.0.0', 'ujson>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'yatb',
    'version': '0.0.2',
    'description': 'Yet Another Telegram Bot implementation',
    'long_description': None,
    'author': 'denolehov',
    'author_email': 'denolehov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
