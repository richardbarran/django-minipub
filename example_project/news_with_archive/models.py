from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

from model_utils import Choices

from minipub.models import MinipubModel


@python_2_unicode_compatible
class Article(MinipubModel):
    STATUS = Choices('draft', 'published', 'archived')

    title = models.CharField(unique=True, max_length=50)
    slug = models.SlugField()
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.status == self.STATUS.archived:
            return reverse('news_with_archive:article_archived_detail', kwargs={'slug': self.slug})
        else:
            return reverse('news_with_archive:article_detail', kwargs={'slug': self.slug})
