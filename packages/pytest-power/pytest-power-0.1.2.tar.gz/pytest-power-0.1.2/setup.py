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
    'version': '0.1.2',
    'description': 'pytest plugin with powerful fixtures',
    'long_description': "# pytest-power\n\n[![PyPI](https://img.shields.io/pypi/v/pytest-power?style=flat-square)](https://pypi.org/project/pytest-power/)\n\nAdds a number of shorthands for fixtures and other helpers for easier testing:\n\n- patch.object\n- patch.init\n- patch.many\n- patch.everything\n\nYou can instal pytest-power with pip:\n\n```sh\npip install pytest-power\n```\n\n## Usage\n\n### patch.object\n\nA shorthand for pytest-mock's `mocker.patch.object`\n\n\n```python\nfrom myapp import App\n\ndef test_app_run(patch):\n  patch.object(App, 'run')\n  App.run()\n  assert App.run.call_count == 1\n```\n\nYou can pass keywords arguments as usual:\n\n```python\nfrom myapp import App\n\ndef test_app_run(patch):\n  patch.object(App, 'run', return_value='running')\n  assert App.run() == 'running'\n```\n\n\n### patch.init\n\nMakes patching `__init__` a bit simpler:\n\n\n```python\nfrom myapp import App\n\ndef test_app_init(patch):\n  patch.init(App)\n  app = App()\n  assert isinstance(app, App)\n```\n\nInstances patched in this way do not have properties that are set in `__init__`,\nso they have to be set again by hand.\n\nKeyword arguments are passed to underlying `patch.object`, and autospec is\nenabled by default.\n\n### patch.many\n\nA shorthand to patch many properties of the same object:\n\n```python\nfrom myapp import App\n\ndef test_app_run_called_by_run(patch):\n  patch.many(App, ['run', 'called_by_run'])\n  App.run()\n  assert App.called_by_run.call_count == 1\n```\n\nKeyword arguments are again passed to underlying `patch.object`, and autospec\nis enabled by default.\n\n### patch.everything\n\nA shorthand to patch every non-magic property. Useful when patch.many gets\ntoo long!\n\n```python\nfrom myapp import App\n\ndef test_app_run_called_by_run(patch):\n  patch.everything(App)\n  App.run()\n  assert App.called_by_run.call_count == 1\n```\n\nNo keyword arguments support...because I forgot!\n",
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
