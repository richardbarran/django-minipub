from django.db.models.query import QuerySet
from django.db.models import Q

import datetime


class MinipubQuerySet(QuerySet):

    def live(self, statuses=['published']):
        today = datetime.date.today()
        return self.filter(status__in=statuses).\
            filter(Q(start__lte=today) | Q(start__isnull=True)).\
            filter(Q(end__gte=today) | Q(end__isnull=True))
