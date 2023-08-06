# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nldata', 'nldata.corpora', 'nldata.nlp']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.20,<0.30.0',
 'cyac>=1.0,<2.0',
 'filelock>=3.0.12,<4.0.0',
 'numpy>=1.19.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'smart_open>=2.0.0,<3.0.0',
 'tqdm>=4.46.1,<5.0.0']

setup_kwargs = {
    'name': 'nldata',
    'version': '0.3.0',
    'description': 'NLData is a library of Natural Language Datasets.',
    'long_description': None,
    'author': 'Davide Nunes',
    'author_email': 'davidenunes@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
