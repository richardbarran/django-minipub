"""

``MininewsModel`` is an abstract model that provides the following 3 fields:

- ``status``: a list of choices; default is 'draft' or 'published'.
- ``start``: a start date; defaults to date of publication.
- ``end``: an end date; optional.

Timestamps
----------
``MininewsModel`` also adds the following read-only fields: ``created``, ``modified`` and ``status_changed``.

The concept of 'Live' objects
-----------------------------

Objects are usually considered 'live' **if** they are 'published'
**and** between the start and end dates - this is usually sufficient for them being available
to display in the public website.

``live()`` methods are available both as a chainable filter on a queryset,
and as an instance method. For example, if you have an ``Article`` model that uses ``MininewsModel``:

.. code-block:: python

    my_articles = Article.objects.live()

or

.. code-block:: python

    can_be_viewed = article1.live()

Refining the concept of a 'Live' object
---------------------------------------

Let's imagine that your articles can be ``published``, but that at some point in time you will want
to manually move them to an 'archived' section in the website.

Models
~~~~~~
First, you will define in your model the complete list of statuses available:

.. code-block:: python

    class MyCustomModel(MininewsModel):

        STATUS = Choices('draft', 'published', 'archived')

And you'll also tweak your ``get_absolute_url()`` to handle the new options:

.. code-block:: python

    def get_absolute_url(self):
        if self.status == self.STATUS.archived:
            return reverse('the_url_for_the_archived_page', kwargs={'slug': self.slug})
        else:
            return reverse('the_url_for_the_published_page', kwargs={'slug': self.slug})

Views
~~~~~
Secondly, in your ``views.py`` you will have 2 sets of views:

- the views for the main pages.
- the views for the archived pages.

And the urls would look something like::

    /news/
    /news/<article slug>/
    /archives/
    /archives/<article slug>/

In the views, you will split out the articles to be displayed in the main section:

.. code-block:: python

    class ArticleDetailView(MininewsDetailView):
        model = Article
        context_object_name = 'article'
        mininews_live = ('published',)

And then the articles to show in the archives section:

.. code-block:: python

    class ArticleArchivesDetailView(MininewsDetailView):
        model = Article
        context_object_name = 'article'
        mininews_live = ('archived',)

We have added a new attribute - ``mininews_live``. This will override the ``STATUS`` defined
on the model.

Sitemaps
~~~~~~~~
If you have defined a sitemap.xml, refer also to the :ref:`sitemaps page<sitemaps-label>`.

"""


from django.db import models
from django.core.exceptions import ValidationError

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices
from model_utils.managers import PassThroughManager

import datetime

from .managers import MininewsQuerySet


class MininewsModel(StatusModel, TimeStampedModel):

    STATUS = Choices('draft', 'published')

    start = models.DateField('start date', null=True, blank=True)
    end = models.DateField('end date', null=True, blank=True)

    objects = PassThroughManager.for_queryset_class(MininewsQuerySet)()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Set the start date for non-draft items if it hasn't been set already."""
        if self.status != self.STATUS.draft and self.start is None:
            self.start = datetime.date.today()
        super(MininewsModel, self).save(*args, **kwargs)

    def clean(self):
        if self.start and self.end and self.start > self.end:
            raise ValidationError('The end date cannot be before the start date.')

    def live(self, statuses=['published']):
        if self.status not in statuses:
            return False
        if self.start and self.start > datetime.date.today():
            return False
        if self.end and self.end < datetime.date.today():
            return False
        return True
    live.boolean = True

    @property
    def staff_preview(self):
        """Helper property - says if this object is being previewed by a member of staff.

        Can be used when displaying objects in the website - members of staff will see all
        objects, using this property in the template can help for attaching a message/custom
        CSS saying that this object is being previewed.

        For example, in the example_project we have this snippet:

        .. code-block:: django

            {% if article.staff_preview %}
                <div class="label label-warning">This is a preview</div>
            {% endif %}

        """

        return self.status == self.STATUS.draft
