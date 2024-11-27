.. _three_scanner:

three.scanner
=============

Overview
--------

The `three.scanner` module provides functionality for scanning and processing data. It is the main part of the `three` library.

Installation
------------

To install the `three` library, use pip:

.. code-block:: bash

    pip install mfthree

Usage
-----

Here is an example of how to use the `three.scanner` module:

.. code-block:: python

    from three.scanner import Scanner

    # Connect
    scanner = Scanner(OnTask=OnTask, OnMessage=None, OnBuffer=None)
    scanner.Connect("ws://matterandform.local:8081")

    # Try to scan without input => Will trigger an error
    scanner.new_scan()

API Reference
-------------

Scanner
~~~~~~~

.. autoclass:: three.scanner.Scanner
    :members:
    :undoc-members:
    :show-inheritance:

Contributing
------------

If you would like to contribute to the `three` library, please refer to the `GITHUB_PAGE`_.

.. _GITHUB_PAGE: https://github.com/Matter-and-Form/three-python-library

License
-------

The `three` library is licensed under the MIT License. See the `LICENSE`_ file for more details.

.. _LICENSE: https://github.com/Matter-and-Form/three-python-library/blob/release/LICENSE