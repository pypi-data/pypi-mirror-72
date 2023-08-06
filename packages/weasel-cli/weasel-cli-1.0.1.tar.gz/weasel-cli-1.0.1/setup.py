# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['weasel']
install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['weasel = weasel:cli']}

setup_kwargs = {
    'name': 'weasel-cli',
    'version': '1.0.1',
    'description': "Simulate Dawkins' weasel experiment",
    'long_description': None,
    'author': 'Wesley Rocha',
    'author_email': 'wesleysr1997@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
