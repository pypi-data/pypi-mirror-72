# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ddv']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['check = tasks:check',
                     'examples = tasks:examples',
                     'flake8 = tasks:flake8',
                     'mypy = tasks:mypy']}

setup_kwargs = {
    'name': 'ddv-printing',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Davide Vitelaru',
    'author_email': 'davide@vitelaru.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
