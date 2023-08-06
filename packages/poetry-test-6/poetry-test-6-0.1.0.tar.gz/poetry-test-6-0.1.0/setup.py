# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_test_6']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'poetry-test-6',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Peter Lin',
    'author_email': 'Peter.Lin@nike.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
