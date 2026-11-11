"""

.. code-block:: python

    from minipub.views import MinipubArchiveIndexView, MinipubYearArchiveView, MinipubDetailView

    class ArticleArchiveView(MinipubArchiveIndexView):
        ...

Minipub provides a few basic views to get you started - but you are encouraged to look at the source
code. The important thing to note is the ``GetQuerysetMixin`` mixin - you can use this with most
of Django's List- and Detail- class based-views to easily integrate minipub.

For example, in minipub' ``views.py``, here is the source code for defining a detail view:

.. code-block:: python

    class MinipubDetailView(GetQuerysetMixin, DetailView):
        pass

"""

from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.views.generic import DetailView
from django.db.models import Q

from .managers import publication_date


class GetQuerysetMixin:
    minipub_live = ('published',)

    def get_allow_future(self):
        return self.request.user.is_staff or super().get_allow_future()

    def get_queryset(self):
        qs = super().get_queryset()
        # Staff can preview drafts and future articles, but not expired articles
        # or statuses belonging to a different section.
        if self.request.user.is_authenticated and self.request.user.is_staff:
            staff_statuses = self.minipub_live + (qs.model.STATUS.draft,)
            return qs.filter(status__in=staff_statuses).filter(
                Q(end__gte=publication_date()) | Q(end__isnull=True)
            )
        return qs.live(statuses=self.minipub_live)


class MinipubArchiveIndexView(GetQuerysetMixin, ArchiveIndexView):
    date_field = 'start'


class MinipubYearArchiveView(GetQuerysetMixin, YearArchiveView):
    date_field = 'start'


class MinipubDetailView(GetQuerysetMixin, DetailView):
    pass
