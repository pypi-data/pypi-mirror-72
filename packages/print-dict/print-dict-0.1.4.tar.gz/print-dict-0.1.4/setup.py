# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['print_dict']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'yapf>=0.30.0,<0.31.0']

entry_points = \
{'console_scripts': ['print-dict = print_dict.cli:cli']}

setup_kwargs = {
    'name': 'print-dict',
    'version': '0.1.4',
    'description': '',
    'long_description': '\n# print-dict\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
