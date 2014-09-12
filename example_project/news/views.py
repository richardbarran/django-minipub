from django.shortcuts import get_object_or_404

from mininews.views import ArticleArchiveView, ArticleYearArchiveView, \
    ArticleDetailView

from .models import Article


class ArticleArchiveView(ArticleArchiveView):
    model = Article
    context_object_name = 'article_list'


class ArticleYearArchiveView(ArticleYearArchiveView):
    model = Article
    context_object_name = 'article_list'

    def get_date_list(self, queryset, date_type='year', ordering='DESC'):
        # TODO: get_date_list() on mininews should be overidden to work on queryset.live().
        return self.model.objects.live().dates('start', date_type, order=ordering)


class ArticleDetailView(ArticleDetailView):
    model = Article
    context_object_name = 'article'

    def get_object(self):
        article = get_object_or_404(self.model, slug=self.kwargs['slug'])
        return self._allowed(article)
