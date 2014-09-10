####################
The user perspective
####################

Django-mininews is a basic tool for controlling the *publication* of objects.

Let's take an example: you have a 'news' application, that just consists of a 
Article model. In the admin interface, we have this:

.. image:: /img/mininews-fieldset.png

All articles have the following 3 fields:

- status: usually 'draft' or 'published'.
- start: start date, defaults to whenever the status is changed to ``published``.
- end: end date; optional.

Articles can only be viewed in the public website **if** they are ``published``
**and** between the start and end dates.

Oh, we also have a fieldset for showing various read-only status fields:

.. image:: /img/mininews-status-fieldset.png

These can be of use for tracking changes to an Article.

And that's it... Mininews is just some boilerplate code, that you will 
reuse again and again throughout a project.