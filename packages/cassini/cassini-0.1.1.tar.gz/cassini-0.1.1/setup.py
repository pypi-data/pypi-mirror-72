# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cassini', 'cassini.compat', 'cassini.defaults']

package_data = \
{'': ['*'], 'cassini.defaults': ['templates/*']}

install_requires = \
['ipywidgets>=7.5,<8.0', 'pandas>=1.0,<2.0']

setup_kwargs = {
    'name': 'cassini',
    'version': '0.1.1',
    'description': 'A tool to structure experimental work, data and analysis using Jupyter Lab.',
    'long_description': None,
    'author': '0Hughman0',
    'author_email': 'rammers2@hotmail.co.uk',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
