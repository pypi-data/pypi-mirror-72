# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['create_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'path-util>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['create = create_cli.cli:cli']}

setup_kwargs = {
    'name': 'create-cli',
    'version': '0.1.2',
    'description': '',
    'long_description': '\n# create-cli\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyalev/create-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
