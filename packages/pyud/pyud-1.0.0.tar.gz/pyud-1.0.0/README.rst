pyud
====

.. image:: https://img.shields.io/codefactor/grade/github/williamwflee/pyud/master
    :target: https://www.codefactor.io/repository/github/williamwflee/pyud
    :alt: CodeFactor grade
.. image:: https://readthedocs.org/projects/pyud/badge/?version=latest
    :target: https://readthedocs.org/projects/pyud/
    :alt: Read the Docs build status
.. image:: https://img.shields.io/pypi/v/pyud
    :target: https://pypi.org/project/pyud/
    :alt: Project version on PyPI
.. image:: https://img.shields.io/pypi/pyversions/pyud
    :target: https://pypi.org/project/pyud/
    :alt: Python versions supported on PyPI

A simple wrapper for the Urban Dictionary API in Python.

Features
--------

- Synchronous and asynchronous clients for the API
- Definition objects for object-style access to definition attributes, and includes all fields
- Full coverage of the known API

Requirements
------------

- **Python 3.6 or higher.** Python 2 is not supported.
- `aiohttp <https://docs.aiohttp.org/en/stable/>`_, version 3.6.2

Installing
----------

You can install directly from PyPI:

.. code:: sh

    python3 -m pip install pyud

On Windows this is:

.. code:: bat

    py -3 -m pip install pyud

Quick Examples
--------------

Synchronous Example
~~~~~~~~~~~~~~~~~~~

.. code:: py

    import pyud

    ud = pyud.Client()
    definitions = ud.define("hello")
    print(definitions[0].word) # Outputs "hello"

Asynchronous Example
~~~~~~~~~~~~~~~~~~~~

.. code:: py

    import asyncio

    import pyud


    async def example():
        ud = pyud.AsyncClient()
        definitions = await ud.define("hello")
        print(definitions[0].word) # Outputs "hello"


    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())

Documentation
-------------

`pyud Documentation <https://pyud.readthedocs.io/en/latest/>`_

License
-------

`GNU GPL v3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_