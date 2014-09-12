############################
Installation & configuration
############################


Installation
------------
The easiest way to install Mininews is to get the latest version from `PyPi <https://pypi.python.org/pypi>`_::

    pip install django-mininews

You can also live dangerously and install the latest code directly from the
Github repository::

    pip install -e git+https://github.com/richardbarran/django-mininews.git#egg=django-mininews

This code should work ok - like `Django <https://www.djangoproject.com/>`_
itself, the master branch should be bug-free. Note however that you will get far better support
if you stick with one of the official releases!

Dependencies
------------

The following dependencies will be installed automatically if required:

* `Django <https://www.djangoproject.com/>`_.
* `Django-model-utils <https://pypi.python.org/pypi/django-model-utils>`_.


Configure Your Django Settings
------------------------------

Add ``mininews`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
         # ...other installed applications,
         'mininews',
    )

You are now ready to use mininews in your code.