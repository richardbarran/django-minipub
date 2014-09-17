from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.views.generic import DetailView


class GetQuerysetMixin(object):

    def get_queryset(self):
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            return self.model.objects.all()
        return self.model.objects.live()


class MininewsArchiveIndexView(GetQuerysetMixin, ArchiveIndexView):
    model = None
    date_field = 'start'
    paginate_by = 20
    # Display page even if no content; this is convenience as in practice the
    # landing page for a blog will be in the main site menu, and it's not nice
    # for that to lead to a 404.
    allow_empty = True


class MininewsYearArchiveView(GetQuerysetMixin, YearArchiveView):
    model = None
    date_field = 'start'
    paginate_by = 20
    make_object_list = True


class MininewsDetailView(GetQuerysetMixin, DetailView):
    model = None
