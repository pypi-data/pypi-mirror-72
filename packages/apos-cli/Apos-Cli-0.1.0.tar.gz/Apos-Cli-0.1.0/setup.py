# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apos_cli']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'datetime>=4.3,<5.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['apos = apos_cli.apos:run']}

setup_kwargs = {
    'name': 'apos-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Florian Vahl',
    'author_email': 'florian@flova.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
