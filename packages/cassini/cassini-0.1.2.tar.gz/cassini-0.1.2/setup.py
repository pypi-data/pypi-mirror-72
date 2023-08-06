# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cassini', 'cassini.compat', 'cassini.defaults']

package_data = \
{'': ['*'], 'cassini.defaults': ['templates/*']}

install_requires = \
['ipywidgets>=7.5,<8.0', 'pandas>=1.0,<2.0']

setup_kwargs = {
    'name': 'cassini',
    'version': '0.1.2',
    'description': 'A tool to structure experimental work, data and analysis using Jupyter Lab.',
    'long_description': '# Cassini\n\nA virtual lab-book framework, using Jupyter Lab and Python. \n\n### Installation\n\n1. `pip install cassini`\n2. Install ``ipywidgets`` Jupyter Lab extension ``conda install -c conda-forge nodejs`` then\n``jupyter labextension install @jupyter-widgets/jupyterlab-manager``\n\nTry it: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/0Hughman0/Cassini/master?urlpath=lab%2Ftree%2Fexamples%2Fdefault%2F)\n\nHead to [Quickstart](https://0hughman0.github.io/Cassini/quickstart.html) to get going.\n',
    'author': '0Hughman0',
    'author_email': 'rammers2@hotmail.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
