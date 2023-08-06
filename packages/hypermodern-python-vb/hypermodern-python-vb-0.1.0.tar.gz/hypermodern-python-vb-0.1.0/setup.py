# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python_vb']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.6.1,<4.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python-vb = '
                     'hypermodern_python_vb.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python-vb',
    'version': '0.1.0',
    'description': 'The hypermodern Python project',
    'long_description': '# hypermodern-python-vb\n\n[![Tests](https://github.com/vinceatbluelabs/hypermodern-python-vb/workflows/Tests/badge.svg)](https://github.com/<your-username>/hypermodern-python/actions?workflow=Tests)\n\nRunthrough of https://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n',
    'author': 'Vince Broz',
    'author_email': 'vince.broz@bluelabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vinceatbluelabs/hypermodern-python-vb',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
