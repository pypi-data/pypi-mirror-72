# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['_4711']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['4711 = _4711:cli']}

setup_kwargs = {
    'name': '4711',
    'version': '0.0.2',
    'description': 'A collection of CLI tools for working with data structures, parsing and formatting',
    'long_description': '# `4711`\n\n**`4711` is a natural number that follows `4710` and that is followed by `4712`. It\'s somewhat of "a large arbitrary number".**\n\n[![pypi](https://badge.fury.io/py/4711.svg)](https://pypi.python.org/pypi/4711/)\n[![Made with Python](https://img.shields.io/pypi/pyversions/4711)](https://www.python.org/)\n[![MIT License](https://img.shields.io/github/license/kalaspuff/4711.svg)](https://github.com/kalaspuff/4711/blob/master/LICENSE)\n\n\nIn this case however, `4711` isn\'t just a number. It\'s a CLI tool (or collection CLI tools if you wish) for working with data structures, parsing values, handling conversion and formatting the output. It\'s written in Python, but doesn\'t require any extensive Python knowledge for use.\n\n*Requires Python 3.6+ and should be run on Unix-like systems such as Linux, BSD, macOS, etc.*\n\n\n## Installation with `pipx` (preferred) or `pip`\n\nIt\'s recommended to install `4711` using `pipx`, which is a tool that stores Python based command line interface applications in their own virtual environment, effectively making it accessible without you having to think about setting up virtualenvs on your own or handle the dependencies.\n\n`pipx` is available at [https://github.com/pipxproject/pipx](https://github.com/pipxproject/pipx).\n\nTo install using `pipx` (depending on how you\'ve installed `pipx` previously, may have to use `sudo`):\n```\n$ pipx install 4711\n```\n\nIf you prefer to install the CLI normally using `pip`, go ahead and run:\n```\n$ pip install 4711\n```\n\n\n## Usage and examples\n\n#### Use-case\n```\n$ 4711 --help\n```\n',
    'author': 'Carl Oscar Aaro',
    'author_email': 'hello@carloscar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kalaspuff/4711',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
