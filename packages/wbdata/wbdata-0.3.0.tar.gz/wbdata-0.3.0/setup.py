# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wbdata']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0', 'decorator>=4.0', 'requests>=2.0', 'tabulate>=0.8.5']

extras_require = \
{'docs': ['sphinx>=2.2'], 'pandas': ['pandas>=0.17']}

setup_kwargs = {
    'name': 'wbdata',
    'version': '0.3.0',
    'description': 'A library to access World Bank data',
    'long_description': "# wbdata\n\n| Branch | Status                                                                                                                                                                                                     |\n|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| master | [![master branch status](https://github.com/OliverSherouse/wbdata/workflows/Tests/badge.svg?branch=master)](https://github.com/OliverSherouse/wbdata/actions?query=workflow%3A%22Tests%22+branch%3Amaster) |\n| dev    | [![dev branch status](https://github.com/OliverSherouse/wbdata/workflows/Tests/badge.svg?branch=dev)](https://github.com/OliverSherouse/wbdata/actions?query=workflow%3A%22Tests%22+branch%3Adev)          |\n\nWbdata is a simple python interface to find and request information from the\nWorld Bank's various databases, either as a dictionary containing full metadata\nor as a [pandas](http://pandas.pydata.org) DataFrame or series. Currently,\nwbdata wraps most of the [World Bank\nAPI](http://data.worldbank.org/developers/api-overview), and also adds some\nconvenience functions for searching and retrieving information.\n\nDocumentation is available at <http://wbdata.readthedocs.org/> .\n",
    'author': 'Oliver Sherouse',
    'author_email': 'oliver@oliversherouse.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
