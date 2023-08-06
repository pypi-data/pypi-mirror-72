# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fatlib', 'fatlib.tests']

package_data = \
{'': ['*']}

install_requires = \
['aif360>=0.3.0,<0.4.0', 'pandas>=1.0.5,<2.0.0', 'scikit-learn>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'fatlib',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Code4Thought',
    'author_email': 'support@code4thought.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
