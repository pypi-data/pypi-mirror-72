# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cfg_cli', 'cfg_cli.clients', 'cfg_cli.errors']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.11,<2.0.0',
 'fire>=0.2.1,<0.3.0',
 'importlib-metadata>=1.7.0,<2.0.0',
 'prompt-toolkit>=3.0.5,<4.0.0',
 'python-jose>=3.1.0,<4.0.0',
 'requests>=2.23.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['prism = cfg_cli.prism_cli:wrapper']}

setup_kwargs = {
    'name': 'cfg-cli',
    'version': '0.1.32',
    'description': "Command-line tool for Cofactor Genomics' products and services.",
    'long_description': None,
    'author': 'Alex Bode',
    'author_email': 'alex_bode@cofactorgenomics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
