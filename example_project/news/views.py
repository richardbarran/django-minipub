from django.shortcuts import render
from django.shortcuts import get_object_or_404

from mininews.views import ArticleArchiveView, ArticleYearArchiveView, \
ArticleDetailView

from .models import Article

class ArticleArchiveView(ArticleArchiveView):
    model = Article
    context_object_name = 'article_list'

class ArticleYearArchiveView(ArticleYearArchiveView):
    model = Article

class ArticleDetailView(ArticleDetailView):
    model = Article
    context_object_name = 'article'

    def get_object(self):
        article = get_object_or_404(self.model, slug=self.kwargs['slug'])
        return self._allowed(article)

