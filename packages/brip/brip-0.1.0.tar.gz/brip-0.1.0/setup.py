# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brip', 'brip.brip', 'brip.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'pydicom>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'brip',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Briana',
    'author_email': 'allenbri25@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
