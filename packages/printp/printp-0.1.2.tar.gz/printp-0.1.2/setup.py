# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['printp']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'input-util>=0.1.2,<0.2.0', 'print-dict>=0.1.4,<0.2.0']

entry_points = \
{'console_scripts': ['printp = printp.cli:cli']}

setup_kwargs = {
    'name': 'printp',
    'version': '0.1.2',
    'description': '',
    'long_description': '\n# printp\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyalev/printp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
