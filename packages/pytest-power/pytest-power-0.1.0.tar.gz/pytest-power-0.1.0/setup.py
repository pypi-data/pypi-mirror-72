# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_power']

package_data = \
{'': ['*']}

install_requires = \
['pytest-mock>=3.1.1,<4.0.0', 'pytest>=5.4.3,<6.0.0']

entry_points = \
{'pytest11': ['pytest_power = pytest_power.pytest_power']}

setup_kwargs = {
    'name': 'pytest-power',
    'version': '0.1.0',
    'description': 'pytest plugin with powerful fixtures',
    'long_description': None,
    'author': 'Jacopo Cascioli',
    'author_email': 'jacopo@nl-ix.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nl-ix/pytest-power',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
