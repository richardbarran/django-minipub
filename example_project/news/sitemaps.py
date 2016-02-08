from minipub.sitemaps import MinipubSitemap

from .models import Article


class NewsSitemap(MinipubSitemap):
    model = Article
