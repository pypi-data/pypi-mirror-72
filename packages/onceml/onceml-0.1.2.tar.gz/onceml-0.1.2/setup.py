# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onceml']

package_data = \
{'': ['*']}

install_requires = \
['mlflow>=1.9.1,<2.0.0',
 'neptune-client>=0.4.117,<0.5.0',
 'path>=13.1,<14.0',
 'typer>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['onceml = onceml.onceml:main']}

setup_kwargs = {
    'name': 'onceml',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'DJ',
    'author_email': 'dujun@ruiking.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
