# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tilingsgui']

package_data = \
{'': ['*'], 'tilingsgui': ['resources/img/png/*', 'resources/img/svg/*']}

install_requires = \
['pyglet>=1.5.5,<2.0.0', 'pyperclip>=1.8.0,<2.0.0', 'tilings>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['tilingsgui = tilingsgui.main:main']}

setup_kwargs = {
    'name': 'tilingsgui',
    'version': '0.1.0',
    'description': 'A graphical user interface for tilings',
    'long_description': '# TilingsGUI',
    'author': 'Permuta Triangle',
    'author_email': 'permutatriangle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PermutaTriangle/tilingsgui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
