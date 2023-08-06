# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['print_dict']

package_data = \
{'': ['*']}

install_requires = \
['yapf>=0.30.0,<0.31.0']

setup_kwargs = {
    'name': 'print-dict',
    'version': '0.1.3',
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
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
