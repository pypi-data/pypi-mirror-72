# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numpy_camera']

package_data = \
{'': ['*']}

install_requires = \
['colorama', 'numpy', 'slurm']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'], 'picamera': ['picamera']}

setup_kwargs = {
    'name': 'numpy-camera',
    'version': '0.0.1',
    'description': '???',
    'long_description': '# Numpy Camera\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
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
