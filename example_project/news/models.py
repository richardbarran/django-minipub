from django.db import models
from django.core.urlresolvers import reverse

from mininews.models import AbstractArticleModel, SEOModel

class Article(AbstractArticleModel, SEOModel):

    title = models.CharField(unique=True, max_length=50)
    slug = models.SlugField()
    body = models.TextField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
