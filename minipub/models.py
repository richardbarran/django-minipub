"""

.. code-block:: python

    from minipub.models import MinipubModel

    class Article(MinipubModel):
        ...

``MinipubModel`` is an abstract model that provides the following 3 fields:

- ``status``: a list of choices; default is 'draft' or 'published'.
- ``start``: a start date; defaults to date of publication.
- ``end``: an end date; optional.

Timestamps
----------
``MinipubModel`` also adds the following fields that get auto-updated and should
not be manually modified: ``created``, ``modified`` and ``status_changed``.

The concept of 'Live' objects
-----------------------------

Objects are usually considered 'live' **if** they are 'published'
**and** between the start and end dates - this is usually sufficient for them being available
to display in the public website.

``live()`` methods are available both as a chainable filter on a queryset,
and as an instance method. For example, if you have an ``Article`` model that uses ``MinipubModel``:

.. code-block:: python

    my_articles = Article.objects.live()

or

.. code-block:: python

    can_be_viewed = article1.live()

Extra statuses
~~~~~~~~~~~~~~
Models can have more statuses than ``draft``, ``published`` -
:ref:`see here for more details<extra_statuses-label>`.

Sitemaps
~~~~~~~~
If you have defined a sitemap.xml, refer also to the :ref:`sitemaps page<sitemaps-label>`.

"""


from django.db import models
from django.core.exceptions import ValidationError
from django import VERSION

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices

import datetime

from .managers import MinipubQuerySet


class MinipubModel(StatusModel, TimeStampedModel):

    STATUS = Choices('draft', 'published')

    start = models.DateField('start date', null=True, blank=True)
    end = models.DateField('end date', null=True, blank=True)

    objects = MinipubQuerySet.as_manager()

    class Meta:
        abstract = True
        if VERSION[0] == 1 and VERSION[1] >= 10:
            default_manager_name = 'objects'

    def save(self, *args, **kwargs):
        """Set the start date for non-draft items if it hasn't been set already."""
        if self.status != self.STATUS.draft and self.start is None:
            self.start = datetime.date.today()
        super(MinipubModel, self).save(*args, **kwargs)

    def clean(self):
        super(MinipubModel, self).clean()
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
