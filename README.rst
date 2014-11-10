Django-mininews
===============

.. image:: https://pypip.in/v/django-mininews/badge.png
    :target: https://crate.io/packages/django-mininews/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/django-mininews/badge.png
    :target: https://crate.io/packages/django-mininews/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/richardbarran/django-mininews.svg?branch=master
    :target: https://travis-ci.org/richardbarran/django-mininews

.. image:: https://coveralls.io/repos/richardbarran/django-mininews/badge.png?branch=master
  :target: https://coveralls.io/r/richardbarran/django-mininews?branch=master

Django-mininews is a basic tool for controlling the *publication* of objects.

Let's take an example: you have a 'news' application, that just consists of a 
Article model. In the admin interface, mininews will add this fieldset:

.. image:: docs/img/mininews-fieldset.png

All articles will have the following 3 fields:

- status: usually 'draft' or 'published'.
- start: start date, defaults to whenever the status is changed to ``published``.
- end: end date; optional.

Articles can only be viewed in the public website **if** they are ``published``
**and** between the start and end dates.

In addition, we have a fieldset for showing various read-only status fields:

.. image:: docs/img/mininews-status-fieldset.png

These can be of use for tracking changes to an Article.

And that's it... Mininews is just an abstract Model, together with plenty of code - in the models,
views, admin and sitemap - to make the best use of it, that you will reuse 
again and again throughout a project.

What can I use it for?
----------------------
Here are some examples of Mininews at work:

- `Minutes of the meetings of an association <http://www.saphra.org.uk/meetings/>`_.
- `Controlling the publication of the Events at a well-known racetrack <http://www.silverstone.co.uk/events/>`_.
- `Controlling when job offers are displayed <http://www.ipglobal-ltd.com/en/about/careers/>`_.

Alternatives
------------
There are several similar projects that take slightly different approaches 
to publication control; usually they introduce more sophisticated control. A well-known
example is `django-reversion <https://github.com/etianen/django-reversion>`_.

Mininews is a very basic publication control tool, but works well on several production 
websites. Its author has found it be a decent compromise between a tool that's too
basic to be useful, and too complex to be understood by its intended end users.

Installation and usage
----------------------
.. image:: https://readthedocs.org/projects/django-mininews/badge/?version=latest
    :target: https://readthedocs.org/projects/django-mininews/?badge=latest
    :alt: Documentation Status
Please take a look at
`the documentation <http://django-mininews.readthedocs.org/en/latest/index.html>`_ on ReadTheDocs.
