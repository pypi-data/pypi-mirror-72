# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inquest',
 'inquest.comms',
 'inquest.injection',
 'inquest.test',
 'inquest.test.embed_test_module',
 'inquest.test.probe_test_module',
 'inquest.utils']

package_data = \
{'': ['*'], 'inquest': ['resources/*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'gql==3.0.0a0',
 'janus>=0.5.0,<0.6.0',
 'pandas>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'inquest',
    'version': '0.4.3',
    'description': '',
    'long_description': None,
    'author': 'Shalom Yiblet',
    'author_email': 'shalom.yiblet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
