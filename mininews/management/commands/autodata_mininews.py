import random
import factory
from datetime import date

from django.core.management.base import NoArgsCommand
from django.contrib.webdesign import lorem_ipsum

from ...factories import ArticleFactory
from ...models import Article


class ArticleFactoryEnriched(ArticleFactory):

    @factory.lazy_attribute
    def body(self):
        # Number of words
        length = random.randint(50, 100)
        return lorem_ipsum.words(length, common=False)

class Command(NoArgsCommand):

    help = 'Create some dummy data for the mininews application for playing around with.'

    def handle_noargs(self, **options):

        # TODO: should prompt user before action.

        Article.objects.all().delete()

        for day in range(1, 15):
            ArticleFactoryEnriched(start=date(day=day,
                                             month=12,
                                             year=2011)
                                   )
        for day in range(1, 15):
            ArticleFactoryEnriched(start=date(day=day,
                                             month=1,
                                             year=2012)
                                   )
