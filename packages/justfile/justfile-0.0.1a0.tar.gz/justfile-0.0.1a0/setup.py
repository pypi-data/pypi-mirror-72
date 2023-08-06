# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['justfile', 'justfile.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'justfile',
    'version': '0.0.1a0',
    'description': 'Just Read, Just Write, Just Right',
    'long_description': "========\nOverview\n========\n\nJust Read, Just Write, Just Right\n\n* Free software: MIT license\n\nJustFile is a Python library that provides a function to either read, write, or append.\n\nIt's pretty straight-foward. No creating a file handle. no ``with``-syntax. Just reading from\na path.\n\nExample\n=======\n\n::\n\n    >>> from justfile.io import read\n    >>> nginx_content = read('/etc/nginx/nginx.conf')\n    >>> nginx_content\n    [[ Whatever's in /etc/nginx/nginx.conf ]]\n\n    >>> # But what if it doesn't exist?\n\n    >>> not_found = read('/file/not/found.txt')\n    >>> not_found\n     None\n\nInstallation\n============\n\n::\n\n    pip install justfile\n\nYou can also install the in-development version with::\n\n    pip install https://gitlab.com/src-r-r/python-justfile/-/archive/master/python-justfile-master.zip\n\n\nDocumentation\n=============\n\n\nhttps://python-justfile.readthedocs.io/\n\n\nDevelopment\n===========\n\nTo run the all tests run::\n\n    python3 -m nose\n\nNote, to combine the coverage data from all the tox environments run:\n\n.. list-table::\n    :widths: 10 90\n    :stub-columns: 1\n\n    - - Windows\n      - ::\n\n            set PYTEST_ADDOPTS=--cov-append\n            tox\n\n    - - Other\n      - ::\n\n            PYTEST_ADDOPTS=--cov-append tox\n",
    'author': 'Jordan Hewitt',
    'author_email': 'srcrr@damngood.pro',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/src-r-r/python-justfile',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
