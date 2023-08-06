# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_htmx', 'django_htmx.templatetags']

package_data = \
{'': ['*'], 'django_htmx': ['static/htmx/*', 'templates/htmx/*']}

install_requires = \
['django>=2.2']

setup_kwargs = {
    'name': 'django-htmx',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'nicokant',
    'author_email': 'niccolocantu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
