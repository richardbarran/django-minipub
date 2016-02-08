from minipub.sitemaps import MinipubSitemap

from .models import Article


class NewsPublishedSitemap(MinipubSitemap):
    model = Article


class NewsArchivedSitemap(MinipubSitemap):
    model = Article
    minipub_live = ('archived',)
