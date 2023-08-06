# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routeros']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'routeros',
    'version': '0.1.0',
    'description': 'Implementation of Mikrotik API',
    'long_description': "# RouterOS\n[![Build Status](https://travis-ci.org/rtician/routeros.svg?branch=master)](https://travis-ci.org/rtician/routeros)\n\nRouterOS is a API client for Mikrotik RouterOS.\n\n### How can I install it?\n```\n$ pip install routeros \n```\nThe usage of a virtualenv is recommended.\n\n### How to use it?\n```python\nIn [1]: from routeros import login\n\nIn [2]: routeros = login('user', 'password', '10.1.0.1')\n\nIn [3]: routeros('/ip/pool/print')\nOut[3]: \n({'.id': '*1', 'name': 'dhcp', 'ranges': '192.168.88.10-192.168.88.254'},\n {'.id': '*2', 'name': 'hs-pool-8', 'ranges': '10.5.50.2-10.5.50.254'})\n\nIn [4]: routeros.close()\n\nIn [5]: \n\n```\n\n### Also can use query\nQuery can consult specific attributes on routeros.\n\n**Methods:**\n\n> - query.has(*args)\n> - query.hasnot(*args)\n> - query.equal(**kwargs)\n> - query.lower(**kwargs)\n> - query.greater(**kwargs)\n\n```python\nIn [1]: from routeros import login\n\nIn [2]: routeros = login('user', 'password', '10.1.0.1')\n\nIn [3]: routeros.query('/ip/pool/print').equal(name='dhcp')\nOut[3]: ({'.id': '*1', 'name': 'dhcp', 'ranges': '192.168.88.10-192.168.88.254'},)\n\nIn [4]: routeros.close()\n\nIn [5]: \n\n```\n\n### How to use non-default (8728) API port for login, such as 9999\n\n```python\nrouteros = login('user', 'password', '10.1.0.1', 9999)\n```\n\n### How to use pre-v6.43 login method\n\n```python\nrouteros = login('user', 'password', '10.1.0.1', 8728, True)\n```\n",
    'author': 'Ramiro Tician',
    'author_email': 'ramirotician@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rtician/routeros',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
