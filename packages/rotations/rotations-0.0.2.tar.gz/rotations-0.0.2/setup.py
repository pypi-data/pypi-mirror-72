# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rotations']

package_data = \
{'': ['*']}

install_requires = \
['numpy']

setup_kwargs = {
    'name': 'rotations',
    'version': '0.0.2',
    'description': 'Reference frame rotation sequences',
    'long_description': '# Rotations\n\n**Under construction**\n\n\n## References\n\n- [Euler_angles](https://en.wikipedia.org/wiki/Euler_angles)\n- [Rotation_formalisms_in_three_dimensions](https://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions)\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/rotations/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
