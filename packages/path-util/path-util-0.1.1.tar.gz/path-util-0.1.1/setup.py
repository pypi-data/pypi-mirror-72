# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['path_util']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'path-util',
    'version': '0.1.1',
    'description': '',
    'long_description': '\n# path-util\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyalev/path-util',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
