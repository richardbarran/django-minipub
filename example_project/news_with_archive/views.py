from mininews.views import MininewsArchiveIndexView, MininewsDetailView

from .models import Article


class ArticleArchiveView(MininewsArchiveIndexView):
    model = Article
    context_object_name = 'article_list'
    allow_empty = True
    mininews_live = ('published',)


class ArticleDetailView(MininewsDetailView):
    model = Article
    context_object_name = 'article'
    mininews_live = ('published',)

class ArticleArchivedArchiveView(MininewsArchiveIndexView):
    model = Article
    context_object_name = 'article_list'
    allow_empty = True
    mininews_live = ('archived',)


class ArticleArchivedDetailView(MininewsDetailView):
    model = Article
    context_object_name = 'article'
    mininews_live = ('archived',)
