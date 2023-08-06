# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dehyphen']

package_data = \
{'': ['*']}

install_requires = \
['clean-text>=0.1.1,<0.2.0', 'flair>=0.5,<0.6', 'unidecode[gpl]>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'dehyphen',
    'version': '0.1.1',
    'description': 'Dehyphenation of broken text (mainly German), e.g., extracted from a PDF',
    'long_description': None,
    'author': 'Johannes Filter',
    'author_email': 'hi@jfilter.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
