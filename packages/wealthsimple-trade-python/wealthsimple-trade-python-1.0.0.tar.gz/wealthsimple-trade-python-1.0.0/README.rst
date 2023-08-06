================
Package Overview
================
A convenient Python wrapper for the Wealthsimple Trade API. Note that this wrapper is Unofficial and is not in any way affiliated with Wealthsimple. Please use at your own risk.

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
    * - package
      - | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/wealthsimple-trade-python/badge/?version=latest
    :target: https://wealthsimple-trade-python.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
    
.. |travis| image:: https://api.travis-ci.org/seansullivan44/Wealthsimple-Trade-Python.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/seansullivan44/Wealthsimple-Trade-Python

.. |requires| image:: https://requires.io/github/seansullivan44/Wealthsimple-Trade-Python/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/seansullivan44/Wealthsimple-Trade-Python/requirements/?branch=master

.. |commits-since| image:: https://img.shields.io/github/commits-since/seansullivan44/Wealthsimple-Trade-Python/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/seansullivan44/Wealthsimple-Trade-Python/compare/v0.0.1...master



.. end-badges



Installation
============

::

    pip install wealthsimple-trade-python

You can also install the in-development version with::

    pip install https://github.com/seansullivan44/Wealthsimple-Trade-Python/archive/master.zip

Getting Started
===============
Download the Wealthsimple Trade app for iOS or Android and create an account. This API wrapper will use your Wealthsimple Trade login credentials to make successful API calls. After creating an account, use your login credentials to create a WSTrade object:
::

    import wealthsimple
    WS = wealthsimple.WSTrade('email', 'password')

Documentation
=============


https://Wealthsimple-Trade-Python.readthedocs.io/

