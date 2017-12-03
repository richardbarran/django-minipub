from minipub.views import MinipubArchiveIndexView, MinipubYearArchiveView, \
    MinipubDetailView

from .models import Article


class ArticleArchiveView(MinipubArchiveIndexView):
    model = Article
    context_object_name = 'article_list'
    # Display page even if no content; this is convenience as in practice the
    # landing page for a blog will be in the main site menu, and it's not nice
    # for that to lead to a 404.
    allow_empty = True


class ArticleYearArchiveView(MinipubYearArchiveView):
    model = Article
    context_object_name = 'article_list'
    date_list_period = 'year'
    make_object_list = True  # Show all articles for that year.

    def get_context_data(self, **kwargs):
        """Not strictly required for the demo - I just prefer for the 'year' view to show
        a sidebar with *all* the years that have articles."""

        context = super(ArticleYearArchiveView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.is_staff:
            qs = self.model.objects.all()
        else:
            qs = self.model.objects.live()
        context['date_list'] = qs.dates('start', 'year', order='DESC')
        return context


class ArticleDetailView(MinipubDetailView):
    model = Article
    context_object_name = 'article'
