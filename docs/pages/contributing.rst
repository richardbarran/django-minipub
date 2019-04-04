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

You'll probably also want to manually install
`Sphinx <http://sphinx.pocoo.org/>`_ if you're going to update the documentation.

Coding style
------------
No surprises here - just try to `follow the conventions used by Django itself
<https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/>`_.

Unit tests
----------
Including unit tests with your contributions will earn you bonus points, maybe even a beer. So write
plenty of tests, and run them from the ``/example_project/`` with a
``python manage.py test``.

There's also a `Tox <https://tox.readthedocs.io/en/latest/index.html>`_ configuration file - so if
you have tox installed, run ``tox`` from the ``/example_project/`` folder, and it will run the entire
test suite against all versions of Python and Django that are supported.

Documentation
-------------
Keeping the documentation up-to-date is very important - so if your code changes
how Django-minipub works, or adds a new feature, please check that the documentation is still accurate, and
update it if required.

We use `Sphinx <http://sphinx.pocoo.org/>`_ to prepare the documentation; please refer to the excellent docs
on that site for help.

.. note::

    The CHANGELOG is part of the documentation, so don't forget to update it!
