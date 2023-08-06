# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['thumbnails',
 'thumbnails.backends',
 'thumbnails.management',
 'thumbnails.management.commands',
 'thumbnails.migrations',
 'thumbnails.south_migrations',
 'thumbnails.tests']

package_data = \
{'': ['*']}

install_requires = \
['da-vinci>=0.2.2,<0.3.0', 'django>=3.0.7,<4.0.0', 'shortuuid>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'cs-django-thumbnails',
    'version': '0.3.3',
    'description': 'A simple Django app to manage image/photo thumbnails. Supports remote/cloud storage systems like Amazon S3.',
    'long_description': None,
    'author': 'Leopoldo Parra',
    'author_email': 'lparra.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
