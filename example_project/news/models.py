from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from mininews.models import MininewsModel


@python_2_unicode_compatible
class Article(MininewsModel):

    title = models.CharField(unique=True, max_length=50)
    slug = models.SlugField()
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})
