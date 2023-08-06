# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome', 'outcome.utils', 'outcome.utils.jinja2']

package_data = \
{'': ['*']}

install_requires = \
['colored>=1.4.2,<2.0.0', 'jinja2>=2.11.2,<3.0.0']

setup_kwargs = {
    'name': 'outcome-utils',
    'version': '1.3.0',
    'description': 'A collection of python utils.',
    'long_description': '# utils-py\n![ci-badge](https://github.com/outcome-co/utils-py/workflows/Checks/badge.svg) ![version-badge](https://img.shields.io/badge/version-1.3.0-brightgreen)\n\nA set of python utilities.\n\n## Usage\n\n```sh\npoetry add outcome-utils\n```\n\n## Development\n\nRemember to run `./pre-commit.sh` when you clone the repository.\n',
    'author': 'Douglas Willcocks',
    'author_email': 'douglas@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/utils-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
