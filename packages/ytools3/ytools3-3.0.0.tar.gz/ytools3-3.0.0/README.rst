########
ytools3
########

.. start short_desc

**Library for validating `yaml` files against schema and selectively dumping nodes from `yaml` (or `json`) documents in `yaml` or `json` format.**

.. end short_desc

This is a port of ``ytools`` ( https://github.com/yaccob/ytools ), which was Python 2 only, to Python 3.

.. start shields 

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/ytools3/latest?logo=read-the-docs
	:target: https://ytools3.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status
	
.. |docs_check| image:: https://github.com/domdfcoding/ytools3/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/ytools3/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/ytools3/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/ytools3
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/ytools3/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/ytools3/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/ytools3/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/ytools3/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/ytools3/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/ytools3/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/ytools3/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/ytools3?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/ytools3?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/ytools3
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/ytools3
	:target: https://pypi.org/project/ytools3/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/ytools3
	:target: https://pypi.org/project/ytools3/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/ytools3
	:target: https://pypi.org/project/ytools3/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/ytools3
	:target: https://pypi.org/project/ytools3/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/ytools3
	:alt: License
	:target: https://github.com/domdfcoding/ytools3/blob/master/LICENSE

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/ytools3
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/ytools3/v3.0.0
	:target: https://github.com/domdfcoding/ytools3/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/ytools3
	:target: https://github.com/domdfcoding/ytools3/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. end shields


Features
---------

* Output ``yaml`` as ``json`` or ``python``

* Output ``json`` as ``yaml`` or ``python`` (provided that there are no duplicate mapping entry in the ``json`` source)

* Extract particular nodes from ``yaml`` and ``json`` files.

	+ If ``yaml`` is used as output format (default) the output is a valid ``yaml`` document.

* Validate ``yaml`` and ``json`` documents.

	+ The ``json-schema`` can be provided in ``yaml`` format as well, which improves readability and writability.

* Preserve order of mapping-keys in ``yaml`` and ``json`` output.

* Multi-document support

	+ Multiple input files

		- ... as well as multiple ``yaml`` documents within a file
		- ... and a combination of both


Installation
--------------

.. start installation

``ytools3`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install ytools3

.. end installation
