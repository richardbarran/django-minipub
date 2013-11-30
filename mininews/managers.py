from django.db.models.query import QuerySet
from django.db.models import Q

import datetime

class ArticleQuerySet(QuerySet):

    def viewable(self):
        """Has an article been published - this is a mix of:
        - status being published.
        - article is within start and end dates.
        """
        return self.filter(status=self.model.STATUS.published).\
            filter(Q(start__lte=datetime.date.today) | Q(start__isnull=True)).\
            filter(Q(end__gte=datetime.date.today) | Q(end__isnull=True))

    def date_list(self, kind='year'):
        """A convenience method - when listing articles, we'll often want to
        show all the years for which we have articles."""
        return self.model.objects.viewable().dates('start', kind, order='DESC')



