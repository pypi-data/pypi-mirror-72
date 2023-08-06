=================
Death to DS_Store
=================


.. image:: https://img.shields.io/pypi/v/dtd.svg
        :target: https://pypi.python.org/pypi/dtd

.. image:: https://img.shields.io/travis/muditbac/dtd.svg
        :target: https://travis-ci.com/muditbac/dtd

.. image:: https://readthedocs.org/projects/dtd/badge/?version=latest
        :target: https://dtd.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Python package to patch all the internal functions to ignore .DS_Store file in Mac


* Free software: MIT license
* Documentation: Usage mentioned below


Features
--------

* Patches pathlib internal functions to ignore .DS_Store file


Examples
--------
Before

.. code-block:: python

    >>> import pathlib
    >>> list(pathlib.Path('./tests').iterdir())
    [PosixPath('tests/.DS_Store'), PosixPath('tests/__init__.py'), PosixPath('tests/__pycache__'), PosixPath('tests/test_dtd.py'), PosixPath('tests/test_pathlib.py')]

After

.. code-block:: python

    >>> import pathlib
    >>> import dtd
    >>> dtd.patch_all()
    >>> list(pathlib.Path('./tests').iterdir())
    [PosixPath('tests/__init__.py'), PosixPath('tests/__pycache__'), PosixPath('tests/test_dtd.py'), PosixPath('tests/test_pathlib.py')]

Quick usage by just importing autopatch

.. code-block:: python

    >>> import pathlib
    >>> from dtd import autopatch
    >>> list(pathlib.Path('./tests').iterdir())
    [PosixPath('tests/__init__.py'), PosixPath('tests/__pycache__'), PosixPath('tests/test_dtd.py'), PosixPath('tests/test_pathlib.py')]


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
