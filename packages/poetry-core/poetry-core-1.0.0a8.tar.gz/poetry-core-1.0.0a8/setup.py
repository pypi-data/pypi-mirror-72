# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry',
 'poetry.core',
 'poetry.core._vendor',
 'poetry.core._vendor.attr',
 'poetry.core._vendor.jsonschema',
 'poetry.core._vendor.jsonschema.benchmarks',
 'poetry.core._vendor.packaging',
 'poetry.core._vendor.pyrsistent',
 'poetry.core._vendor.tomlkit',
 'poetry.core.json',
 'poetry.core.masonry',
 'poetry.core.masonry.builders',
 'poetry.core.masonry.utils',
 'poetry.core.packages',
 'poetry.core.packages.constraints',
 'poetry.core.packages.utils',
 'poetry.core.semver',
 'poetry.core.spdx',
 'poetry.core.utils',
 'poetry.core.vcs',
 'poetry.core.version']

package_data = \
{'': ['*'],
 'poetry.core': ['_vendor/jsonschema/schemas/*',
                 'json/schemas/*',
                 'spdx/data/*']}

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['pathlib2>=2.3.5,<3.0.0',
                                                         'typing>=3.7.4.1,<4.0.0.0',
                                                         'enum34>=1.1.10,<2.0.0',
                                                         'functools32>=3.2.3-2,<4.0.0']}

setup_kwargs = {
    'name': 'poetry-core',
    'version': '1.0.0a8',
    'description': 'Core utilities for Poetry',
    'long_description': '',
    'author': 'Sébastien Eustace',
    'author_email': 'sebastien@eustace.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-poetry/core',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
