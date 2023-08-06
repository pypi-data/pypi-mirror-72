# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_picnic_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'python-picnic-api',
    'version': '0.1.0',
    'description': '',
    'long_description': 'python_picnic_api\n=================\n\npython wrapper around the Picnic API',
    'author': 'Mike Brink',
    'author_email': 'mjh.brink@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MikeBrink/python-picnic-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
