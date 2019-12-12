from django.db import models
from django.urls import reverse

from minipub.models import MinipubModel


class Article(MinipubModel):
    title = models.CharField(unique=True, max_length=50)
    slug = models.SlugField()
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})
