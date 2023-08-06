# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyrolint']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=0.3.7,<0.4.0']

setup_kwargs = {
    'name': 'pyrolint',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Steve Dignam',
    'author_email': 'steve@dignam.xyz',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
