========
Overview
========

Just Read, Just Write, Just Right

* Free software: MIT license

JustFile is a Python library that provides a function to either read, write, or append.

It's pretty straight-foward. No creating a file handle. no ``with``-syntax. Just reading from
a path.

Example
=======

::

    >>> from justfile.io import read
    >>> nginx_content = read('/etc/nginx/nginx.conf')
    >>> nginx_content
    [[ Whatever's in /etc/nginx/nginx.conf ]]

    >>> # But what if it doesn't exist?

    >>> not_found = read('/file/not/found.txt')
    >>> not_found
     None

Installation
============

::

    pip install justfile

You can also install the in-development version with::

    pip install https://gitlab.com/src-r-r/python-justfile/-/archive/master/python-justfile-master.zip


Documentation
=============


https://python-justfile.readthedocs.io/


Development
===========

To run the all tests run::

    python3 -m nose

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
