========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |requires| image:: https://requires.io/github/ritzKraka/python-batchelor/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ritzKraka/python-batchelor/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/ritzKraka/python-batchelor/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ritzKraka/python-batchelor

.. |version| image:: https://img.shields.io/pypi/v/batchelor.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/batchelor

.. |wheel| image:: https://img.shields.io/pypi/wheel/batchelor.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/batchelor

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/batchelor.svg
    :alt: Supported versions
    :target: https://pypi.org/project/batchelor

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/batchelor.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/batchelor

.. |commits-since| image:: https://img.shields.io/github/commits-since/ritzKraka/python-batchelor/v0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/ritzKraka/python-batchelor/compare/v0.1...master



.. end-badges

A simple, yet effective batching system using threadpoolexecutor.

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install batchelor

You can also install the in-development version with::

    pip install https://github.com/ritzKraka/python-batchelor/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import batchelor
    batch = batchelor.Batch(enumerate(['my', 'dataset']))
    # batch.help() # for basic help
    batch.start(lambda index, item: print(index, item))  # replace lambda with your function


Development
===========

To run the all tests run::

    tox

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
