# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'k0d-expert',
    'version': '0.0.1',
    'description': 'Cli для школы k0d.expert',
    'long_description': '# Cli для школы k0d.expert\n\n',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://k0d.expert',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
