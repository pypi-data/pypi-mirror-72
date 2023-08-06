# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopystomp', 'aiopystomp.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiopystomp',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'pengyj',
    'author_email': 'p15281826276@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
