# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autosocks']

package_data = \
{'': ['*']}

install_requires = \
['gera2ld.socks>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['autosocks = autosocks.__main__:main']}

setup_kwargs = {
    'name': 'autosocks',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gerald',
    'author_email': 'gera2ld@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
