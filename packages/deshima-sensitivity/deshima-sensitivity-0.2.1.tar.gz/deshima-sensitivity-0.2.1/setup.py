# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deshima_sensitivity']

package_data = \
{'': ['*'], 'deshima_sensitivity': ['data/*']}

install_requires = \
['ipython>=5.5,<6.0',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.17,<2.0',
 'pandas>=0.25,<1.1',
 'scipy>=1.4,<2.0']

setup_kwargs = {
    'name': 'deshima-sensitivity',
    'version': '0.2.1',
    'description': 'Sensitivity calculator for DESHIMA-type spectrometers',
    'long_description': None,
    'author': 'Akira Endo',
    'author_email': 'a.endo@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
