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
    'version': '0.1.5',
    'description': 'A command line interface for APOS the Agile Pizza Ordering Service.',
    'long_description': '# APOS CLI\nA command line interface for APOS the Agile Pizza Ordering Service.\n\n## Usage\nAPOS simplifies ordering pizza with many people e.g. at university events.\nThis simple cli allows you to create group orders or add items (e.g. pizza) to an existing group order.\n\n## This project is still work in progress and pre alpha.\nFeatures change frequently.\nTherefore a proper README follow in a later stage of the project.\n',
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
