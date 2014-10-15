from mininews.sitemaps import MininewsSitemap

from .models import Article


class NewsPublishedSitemap(MininewsSitemap):
    model = Article


class NewsArchivedSitemap(MininewsSitemap):
    model = Article
    mininews_live = ('archived',)
