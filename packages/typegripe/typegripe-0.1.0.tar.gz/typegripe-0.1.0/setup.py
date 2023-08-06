# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typegripe']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'typegripe',
    'version': '0.1.0',
    'description': "mypy tests for correct type annotations. typegripe complains if you didn't add any.",
    'long_description': None,
    'author': 'Matt White',
    'author_email': 'code@typenil.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
