from minipub.views import MinipubArchiveIndexView, MinipubDetailView

from .models import Article


class ArticleArchiveView(MinipubArchiveIndexView):
    model = Article
    context_object_name = 'article_list'
    allow_empty = True
    minipub_live = ('published',)


class ArticleDetailView(MinipubDetailView):
    model = Article
    context_object_name = 'article'
    minipub_live = ('published',)


class ArticleArchivedArchiveView(MinipubArchiveIndexView):
    model = Article
    context_object_name = 'article_list'
    allow_empty = True
    minipub_live = ('archived',)


class ArticleArchivedDetailView(MinipubDetailView):
    model = Article
    context_object_name = 'article'
    minipub_live = ('archived',)
