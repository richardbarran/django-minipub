from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils import timezone


def publication_date():
    """Use the site's calendar, regardless of an activated visitor time zone."""
    now = timezone.now()
    if timezone.is_aware(now):
        return timezone.localdate(now, timezone.get_default_timezone())
    return now.date()


class MinipubQuerySet(QuerySet):

    def live(self, statuses=['published']):
        today = publication_date()
        return self.filter(status__in=statuses).\
            filter(Q(start__lte=today) | Q(start__isnull=True)).\
            filter(Q(end__gte=today) | Q(end__isnull=True))
