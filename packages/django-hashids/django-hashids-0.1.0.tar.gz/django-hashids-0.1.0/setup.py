# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_hashids']

package_data = \
{'': ['*']}

install_requires = \
['hashids>=1.0.2']

setup_kwargs = {
    'name': 'django-hashids',
    'version': '0.1.0',
    'description': 'Non-intrusive hashids library Django',
    'long_description': None,
    'author': 'Shen Li',
    'author_email': 'dustet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6,<4',
}


setup(**setup_kwargs)
