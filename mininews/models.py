from django.db import models
from django.core.exceptions import ValidationError

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices
from model_utils.managers import PassThroughManager

import datetime
import decimal

from .managers import ArticleQuerySet

class AbstractArticleModel(StatusModel, TimeStampedModel):
    """

    'Viewable'
    ----------
    All articles have the following 3 fields:
    - status: 'draft' or 'published'.
    - start: start date, defaults to time of publication.
    - end: end date; optional.
    
    Articles can only be viewed in the front end if they are 'published'
    and between the start and end dates.
    
    ``viewable()`` methods are available both as chainable filters on a queryset,
    and as instance methods.

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

    def viewable(self):
        """Can this article be viewed?"""
        if not self.status == self.STATUS.published:
            return False
        if self.start and self.start > datetime.date.today():
            return False
        if self.end and self.end < datetime.date.today():
            return False
        return True
    viewable.boolean = True

def validate_priority(value):
    if value < decimal.Decimal('0') or value > decimal.Decimal('1.0'):
        raise ValidationError(u'Please enter a number between 0 and 1')

class SEOModel(models.Model):
    """SEO fields are split out into their own mixin; the reasoning is that
    on multilingual sites we might want to i18n the meta fields, and so not
    include this mixin."""

    # SEO fields.
    meta_description = models.CharField(max_length=155,
                                        null=True, blank=True,
                                     help_text='<a href="http://en.wikipedia.org/wiki/Meta_element#The_description_attribute" target="_blank">See here for information.</a>')
    meta_keywords = models.CharField(max_length=255,
                                     null=True, blank=True,
                                     help_text='<a href="http://en.wikipedia.org/wiki/Meta_element#The_keywords_attribute" target="_blank">See here for information.</a>')
    sitemap_priority = models.DecimalField('Priority',
                                           # Don't need 3 digits, but easy way to
                                           # make the validation message a bit cleaner.
                                           max_digits=3,
                                           decimal_places=1,
                                           default=0.5,
                                           validators=[validate_priority],
                                           help_text='Set in the search engine sitemap '
        'the priority of this page relative to other pages in the same site. Use a '
        'value between 0 and 1 - 0.5 is the default.')

    class Meta:
        abstract = True






