from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.views.generic import DetailView


class GetQuerysetMixin(object):

    def get_queryset(self):
        qs = super(GetQuerysetMixin, self).get_queryset()
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            return qs
        return qs.live()


class MininewsArchiveIndexView(GetQuerysetMixin, ArchiveIndexView):
    date_field = 'start'


class MininewsYearArchiveView(GetQuerysetMixin, YearArchiveView):
    date_field = 'start'


class MininewsDetailView(GetQuerysetMixin, DetailView):
    pass
