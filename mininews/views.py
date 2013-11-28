from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Article

class ArticleArchiveView(ArchiveIndexView):
    model = Article
    date_field = 'start'
    paginate_by = 20
    context_object_name = 'article_list'

    def get_queryset(self):
        return self.model.objects.viewable()

class ArticleYearArchiveView(YearArchiveView):
    model = Article
    date_field = 'start'
    paginate_by = 20
    make_object_list = True

    def get_queryset(self):
        return self.model.objects.viewable()

    def get_context_data(self, **kwargs):
        context = super(ArticleYearArchiveView, self).get_context_data(**kwargs)
        dates_qs = self.get_queryset()
        context['date_list'] = self.get_date_list(dates_qs,
                                                  date_type='year',
                                                  ordering='DESC')
        return context

class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'

    def _allowed(self, article):
        """Factor out a bit of boilerplate."""
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            return article
        if not article.viewable():
            raise Http404
        return article

    def get_object(self):
        article = get_object_or_404(self.model, slug=self.kwargs['slug'])
        return self._allowed(article)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        dates_qs = self.model.objects.viewable()
        context['date_list'] = dates_qs.dates('start', 'year')[::-1]
        return context

