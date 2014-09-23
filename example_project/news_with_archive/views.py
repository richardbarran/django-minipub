from mininews.views import MininewsArchiveIndexView, MininewsDetailView

from .models import Article


class ArticleArchiveView(MininewsArchiveIndexView):
    model = Article
    context_object_name = 'article_list'
    # Display page even if no content; this is convenience as in practice the
    # landing page for a blog will be in the main site menu, and it's not nice
    # for that to lead to a 404.
    allow_empty = True


class ArticleDetailView(MininewsDetailView):
    model = Article
    context_object_name = 'article'
