# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonny_blocks']

package_data = \
{'': ['*']}

install_requires = \
['lonny_aws_blob>=0.1.1,<0.2.0',
 'lonny_aws_stack>=0.2.1,<0.3.0',
 'troposphere>=2.6.1,<3.0.0']

setup_kwargs = {
    'name': 'lonny-blocks',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'tlonny',
    'author_email': 't@lonny.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
