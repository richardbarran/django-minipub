Django-minipub
===============

.. image:: https://img.shields.io/pypi/v/django-minipub.svg
    :target: https://pypi.python.org/pypi/django-minipub/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-minipub.svg
    :target: https://pypi.python.org/pypi/django-minipub/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/richardbarran/django-minipub.svg?branch=master
    :target: https://travis-ci.org/richardbarran/django-minipub

.. image:: https://coveralls.io/repos/richardbarran/django-minipub/badge.png?branch=master
  :target: https://coveralls.io/r/richardbarran/django-minipub?branch=master

Django-minipub is a **mini**-malist **pub**-lication control system for Django.

Let's take an example: you have a 'news' application, with an 
Article model. In the admin interface, minipub will add this fieldset:

.. image:: docs/img/minipub-fieldset.png

All articles will then have the following 3 fields:

- status: usually ``draft`` or ``published``.
- start: start date.
- end: end date; optional.

Articles will only be visible in the public website **if** they are ``published``
**and** today's date is between the start and end dates.

In addition, we have a fieldset for showing various read-only status fields:

.. image:: docs/img/minipub-status-fieldset.png

These can be of use for tracking changes to an Article.

And that's it... Minipub is just a few fields on a Model Mixin, together with plenty of code - in the models,
views, admin and sitemap - to make the best use of it, that you will hopefully reuse 
again and again throughout a project.

What can I use it for?
----------------------
Here are some examples of Minipub at work:

- `Minutes of the meetings of an association <http://www.saphra.org.uk/meetings/>`_.
- `Controlling the publication of the Events at a well-known racetrack <http://www.silverstone.co.uk/events/>`_.
- `Controlling when job offers are displayed <http://www.ipglobal-ltd.com/en/about/careers/>`_.

Alternatives
------------
There are several similar projects that take slightly different approaches 
to publication control; usually they introduce more sophisticated control. A well-known
example is `django-reversion <https://github.com/etianen/django-reversion>`_.

Minipub is a very basic publication control tool, but works well on several production 
websites. Its author has found it be a decent compromise between a tool that's too
basic to be useful, and too complex to be understood by its intended end users.

Installation and usage
----------------------
.. image:: https://readthedocs.org/projects/django-minipub/badge/?version=latest
    :target: https://readthedocs.org/projects/django-minipub/?badge=latest
    :alt: Documentation Status
Please take a look at
`the documentation <http://django-minipub.readthedocs.org/en/latest/index.html>`_ on ReadTheDocs.
