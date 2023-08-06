# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gogogate2_api']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.2',
 'defusedxml>=0.6.0',
 'pycryptodomex>=3.9.7',
 'requests>=2.23.0',
 'typing-extensions>=3.7.4.2']

setup_kwargs = {
    'name': 'gogogate2-api',
    'version': '1.0.4',
    'description': 'Library for connecting to gogogate2 hubs',
    'long_description': '# Python gogogate2-api [![Build status](https://github.com/vangorra/python_gogogate2_api/workflows/Build/badge.svg?branch=master)](https://github.com/vangorra/python_gogogate2_api/actions?workflow=Build) [![codecov](https://codecov.io/gh/vangorra/python_gogogate2_api/branch/master/graph/badge.svg)](https://codecov.io/gh/vangorra/python_gogogate2_api) [![PyPI](https://img.shields.io/pypi/v/gogogate2-api)](https://pypi.org/project/gogogate2-api/)\nPython library for controlling gogogate2 devices\n\n\n## Installation\n\n    pip install gogogate2-api\n\n## Usage\nFor a complete example, checkout the integration test in `scripts/integration_test.py`. It has a working example on how to use the API.\n```python\nfrom gogogate2_api import GogoGate2Api\napi = GogoGate2Api("10.10.0.23", "admin", "password")\n\n# Get info about device and all doors.\napi.info()\n\n# Open/close door.\napi.open_door(1)\napi.close_door(1)\n```\n\n## Building\nBuilding, testing and lintings of the project is all done with one script. You only need a few dependencies.\n\nDependencies:\n- python3 in your path.\n- The python3 `venv` module.\n\nThe build script will setup the venv, dependencies, test and lint and bundle the project.\n```bash\n./scripts/build.sh\n```\n',
    'author': 'Robbie Van Gorkom',
    'author_email': 'robbie.van.gorkom@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vangorra/python_gogogate2_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
