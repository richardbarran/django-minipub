from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.views.generic import DetailView
from django.http import Http404


class MininewsArchiveIndexView(ArchiveIndexView):
    model = None
    date_field = 'start'
    paginate_by = 20
    # Display page even if no content; this is convenience as in practice the
    # landing page for a blog will be in the main site menu, and it's not nice
    # for that to lead to a 404.
    allow_empty = True

    def get_queryset(self):
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            return self.model.objects.all()
        return self.model.objects.live()


class MininewsYearArchiveView(YearArchiveView):
    model = None
    date_field = 'start'
    paginate_by = 20
    make_object_list = True

    def get_queryset(self):
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            return self.model.objects.all()
        return self.model.objects.live()


class MininewsDetailView(DetailView):
    model = None

    def _allowed(self, article, statuses=None):
        """Factor out a bit of boilerplate."""
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            return article
        if statuses:
            if not article.live(statuses):
                raise Http404
        else:
            if not article.live():
                raise Http404
        return article
