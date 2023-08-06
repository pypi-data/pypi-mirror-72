# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ya_activity',
 'ya_activity.api',
 'ya_activity.models',
 'ya_market',
 'ya_market.api',
 'ya_market.models',
 'ya_payment',
 'ya_payment.api',
 'ya_payment.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'ya-aioclient',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Przemysław K. Rekucki',
    'author_email': 'prekucki@rcl.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
