# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['print_pretty']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'input-util>=0.1.2,<0.2.0',
 'print-dict>=0.1.3,<0.2.0',
 'pyyaml>=5.3.1,<6.0.0',
 'yapf>=0.30.0,<0.31.0']

entry_points = \
{'console_scripts': ['print-pretty = print_pretty.cli:cli']}

setup_kwargs = {
    'name': 'print-pretty',
    'version': '0.1.1',
    'description': '',
    'long_description': '\n# print-pretty\n\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyalev/print-pretty',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
