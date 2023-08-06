# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sprite_pack']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=14.0,<15.0',
 'pillow>=7.1.2,<8.0.0',
 'rectangle-packer>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['sprite-pack = sprite_pack:main']}

setup_kwargs = {
    'name': 'sprite-pack',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Gregory C. Oakes',
    'author_email': 'gregoryoakes@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
