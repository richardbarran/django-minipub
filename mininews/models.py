from django.db import models
from django.core.exceptions import ValidationError

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices
from model_utils.managers import PassThroughManager

import datetime

from .managers import ArticleQuerySet


class AbstractArticleModel(StatusModel, TimeStampedModel):

    """

    'Viewable'
    ----------
    All articles have the following 3 fields:
    - status: usually 'draft' or 'published'.
    - start: start date, defaults to time of publication.
    - end: end date; optional.
    
    Articles can only be viewed in the front end if they are 'published'
    and between the start and end dates.
    
    ``viewable()`` methods are available both as chainable filters on a queryset,
    and as instance methods.

    ``viewable()`` take one optional argument: ``statuses``. This is for when you change
    the status list; for example, if you define::

        STATUS = Choices('draft', 'published', 'archived')    

    Then the notion of ``viewable`` will depend if you are in the section of the site that
    shows the ``published`` articles, or in the section that shows the ``archived`` articles.

    So you can specify what makes an article ``viewable``; the default is ``published``.


    """

    STATUS = Choices('draft', 'published')

    # NB: start is a required field, as it is used for sorting the articles in
    # the archive views.
    start = models.DateField('start date', null=True, blank=True)
    end = models.DateField('end date', null=True, blank=True)

    objects = PassThroughManager.for_queryset_class(ArticleQuerySet)()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Set the publication date for published items if it hasn't been set already."""
        if self.status == self.STATUS.published and self.start is None:
            self.start = datetime.date.today()
        super(AbstractArticleModel, self).save(*args, **kwargs)

    def clean(self):
        if self.start and self.end and self.start > self.end:
            raise ValidationError('The end date cannot be before the start date.')

    def viewable(self, statuses=['published']):
        """Can this article be viewed?"""
        if not self.status in statuses:
            return False
        if self.start and self.start > datetime.date.today():
            return False
        if self.end and self.end < datetime.date.today():
            return False
        return True
    viewable.boolean = True
