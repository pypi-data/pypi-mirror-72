# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ctorch', 'ctorch.nn', 'ctorch.nn.modules']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'ctorch',
    'version': '0.1.0',
    'description': 'Complex Neural Networks for PyTorch',
    'long_description': None,
    'author': 'Miller Wilt',
    'author_email': 'miller@pyriteai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
