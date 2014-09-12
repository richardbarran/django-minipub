from django.db.models.query import QuerySet
from django.db.models import Q

import datetime


class MininewsQuerySet(QuerySet):

    def live(self, statuses=['published']):
        return self.filter(status__in=statuses).\
            filter(Q(start__lte=datetime.date.today) | Q(start__isnull=True)).\
            filter(Q(end__gte=datetime.date.today) | Q(end__isnull=True))
