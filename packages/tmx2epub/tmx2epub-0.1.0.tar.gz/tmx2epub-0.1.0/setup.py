# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tmx2epub']

package_data = \
{'': ['*']}

install_requires = \
['EbookLib>=0.17.1,<0.18.0',
 'absl-py>=0.9.0,<0.10.0',
 'logzero>=1.5.0,<2.0.0',
 'more_itertools>=8.4.0,<9.0.0',
 'pyquery>=1.4.1,<2.0.0',
 'tqdm>=4.47.0,<5.0.0']

entry_points = \
{'console_scripts': ['tmx2epub = tmx2epub.__main__:main']}

setup_kwargs = {
    'name': 'tmx2epub',
    'version': '0.1.0',
    'description': 'converts tmx to epub',
    'long_description': '# tmx2epub ![build](https://github.com/ffreemt/xtl-read-assistant/workflows/build/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/xtl-read-assistant/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/xtl-read-assistant)[![CodeFactor](https://www.codefactor.io/repository/github/ffreemt/xtl-read-assistant/badge/master)](https://www.codefactor.io/repository/github/ffreemt/xtl-read-assistant/overview/master)[![PyPI version](https://badge.fury.io/py/xtl-read-assistant.svg)](https://badge.fury.io/py/xtl-read-assistant)\nconvert tmx to epub\n\n### Installation\n```pip install tmx2epub```\n\n### Usage\n\n#### Casual\nRun `tmx2epub.exe` and browse to select a tmx/gz/bzip2 file.\n\n#### Adavanced\n`tmx2epub.exe --helpshort`\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/tmx2epub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
