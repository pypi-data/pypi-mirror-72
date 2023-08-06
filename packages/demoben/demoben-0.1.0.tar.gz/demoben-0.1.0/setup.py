# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demoben']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.5,<2.0.0']

setup_kwargs = {
    'name': 'demoben',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ben-Cheng',
    'author_email': 'bcheng@linz.govt.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
