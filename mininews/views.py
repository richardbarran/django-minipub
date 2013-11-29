from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.views.generic import DetailView
from django.http import Http404

class ArticleArchiveView(ArchiveIndexView):
    model = None
    date_field = 'start'
    paginate_by = 20
    # Display page even if no content; this is convenience as in practice the
    # landing page for a blog will be in the main site menu, and it's not nice
    # for that to lead to a 404.
    allow_empty = True

    def get_queryset(self):
        return self.model.objects.viewable()

class ArticleYearArchiveView(YearArchiveView):
    model = None
    date_field = 'start'
    paginate_by = 20
    make_object_list = True

    def get_queryset(self):
        return self.model.objects.viewable()

class ArticleDetailView(DetailView):
    model = None

    def _allowed(self, article):
        """Factor out a bit of boilerplate."""
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            return article
        if not article.viewable():
            raise Http404
        return article


