##############################
Contributing to Django-minipub
##############################

Contributions are always very welcome. Even if you have never contributed to an
open-source project before - please do not hesitate to offer help. Fixes for typos in the
documentation, extra unit tests, etc... are all welcome.

Example project
---------------
Django-minipub includes an example project under ``/example_project/`` to get you quickly ready for
contributing to the project - do not hesitate to use it!

Install the project and development dependencies from the repository root::

    python -m pip install -e '.[dev,docs]'

Coding style
------------
No surprises here - just try to `follow the conventions used by Django itself
<https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/>`_.

Unit tests
----------
Including unit tests with your contributions will earn you bonus points, maybe even a beer. So write
plenty of tests, and run them from the repository root with ``bin/test.py``.

There's also a `Tox <https://tox.readthedocs.io/en/latest/index.html>`_ configuration file - so if
you have tox installed, run ``tox`` from the repository root, and it will run the entire
test suite against all versions of Python and Django that are supported.

Documentation
-------------
Keeping the documentation up-to-date is very important - so if your code changes
how Django-minipub works, or adds a new feature, please check that the documentation is still accurate, and
update it if required.

We use `Sphinx <https://www.sphinx-doc.org/>`_ to prepare the documentation.
Build it from the repository root with warnings treated as errors::

    python -m sphinx -E -W --keep-going -b html docs docs/_build/html

The local prerelease check validates documentation; CI does not build it.
Read the Docs publishes documentation when a release tag is pushed; see
:doc:`releasing` for the release and recovery process.

.. note::

    The CHANGELOG is part of the documentation, so don't forget to update it!
