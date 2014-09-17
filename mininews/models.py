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

Imagine that your articles can be ``published``,
but that at some point in time you will want to manually move them to an 'archived'
section in the website.

In your article model (that inherits from ``MininewsModel``) you would define::

    STATUS = Choices('draft', 'published', 'archived')    

Then the notion of 'live' will depend if you are in the section of the site that
shows the ``published`` articles, or in the section that shows the ``archived`` articles.

You would have in your ``views.py`` 2 sets of views:

- for the main pages.
- for the archived pages.

In each of these you would define what status (or statuses) make an article 'live'.

``live()`` take one optional argument: ``statuses``. This is for when you change
the list of status choices; for example...



"""


from django.db import models
from django.core.exceptions import ValidationError

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices
from model_utils.managers import PassThroughManager

import datetime

from .managers import MininewsQuerySet


class MininewsModel(StatusModel, TimeStampedModel):

    # TODO: add a property to the model so that in the template we can
    # highlight not-live articles.

    STATUS = Choices('draft', 'published')

    # TODO: start is a required field when published, as it is used for sorting the articles in
    # the archive views.
    start = models.DateField('start date', null=True, blank=True)
    end = models.DateField('end date', null=True, blank=True)

    objects = PassThroughManager.for_queryset_class(MininewsQuerySet)()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Set the publication date for published items if it hasn't been set already."""
        # TODO: if an article is set to 'archived' it should also trigger the start date.
        if self.status == self.STATUS.published and self.start is None:
            self.start = datetime.date.today()
        super(MininewsModel, self).save(*args, **kwargs)

    def clean(self):
        # TODO: fail we are setting 'published' and the end date is in the past?
        if self.start and self.end and self.start > self.end:
            raise ValidationError('The end date cannot be before the start date.')

    def live(self, statuses=['published']):
        # TODO: an object cannot be 'live' if its start date is not set.
        if not self.status in statuses:
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
