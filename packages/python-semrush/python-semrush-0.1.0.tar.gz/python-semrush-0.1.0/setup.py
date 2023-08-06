# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_semrush', 'python_semrush.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'python-semrush',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tulio Cesar Martins Pereira',
    'author_email': 'funroll.loops@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
