############################
Installation & configuration
############################


Installation
------------
The easiest way to install Minipub is to get the latest version from `PyPi <https://pypi.org/>`_::

    pip install django-minipub

You can also live dangerously and install the latest code directly from the
Github repository::

    pip install -e git+https://github.com/richardbarran/django-minipub.git#egg=django-minipub

This code should work ok - like `Django <https://www.djangoproject.com/>`_
itself, the master branch should be bug-free. Note however that you will get far better support
if you stick with one of the official releases!

Dependencies
------------

The following dependencies will be installed automatically if required:

* `Django <https://www.djangoproject.com/>`_.
* `Django-model-utils <https://pypi.org/project/django-model-utils/>`_.


Configure Your Django Settings
------------------------------

Add ``minipub`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
         # ...other installed applications,
         'minipub',
    )

You are now ready to use minipub in your code.
