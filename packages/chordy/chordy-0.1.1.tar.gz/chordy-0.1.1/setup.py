# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chordy']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'regex>=2020.6.8,<2021.0.0']

setup_kwargs = {
    'name': 'chordy',
    'version': '0.1.1',
    'description': 'Small library to work with chords and chord-annotated songs',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
