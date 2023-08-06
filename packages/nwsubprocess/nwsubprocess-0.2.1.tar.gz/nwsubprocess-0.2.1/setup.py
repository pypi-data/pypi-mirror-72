# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nwsubprocess']

package_data = \
{'': ['*']}

install_requires = \
['atomicwrites', 'psutil']

setup_kwargs = {
    'name': 'nwsubprocess',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'NativeWaves',
    'author_email': 'contact@nativewaves.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
