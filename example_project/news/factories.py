from django.utils.text import slugify

import factory

from .models import Article


class ArticleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Article

    # Create some dummy default values for the title (which has to be unique).
    title = factory.Sequence(lambda n: f'article{n:0>3}')
    slug = factory.LazyAttribute(lambda a: slugify(f'{a.title}'))
    status = Article.STATUS.published
