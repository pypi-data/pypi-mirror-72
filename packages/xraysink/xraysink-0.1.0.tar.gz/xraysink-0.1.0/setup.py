# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xraysink', 'xraysink.asgi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xraysink',
    'version': '0.1.0',
    'description': 'Extra integrations for AWS X-RAY and asyncio Python.',
    'long_description': '# xraysink\nExtra integrations for AWS X-RAY and asyncio Python.\n\n\n## Licence\nThis project uses the Apache 2.0 licence, to make it compatible with the primary\n[aws_xray_sdk](https://github.com/aws/aws-xray-sdk-python) library.',
    'author': 'Gary Donovan',
    'author_email': 'gazza@gazza.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/garyd203/xraysink',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
