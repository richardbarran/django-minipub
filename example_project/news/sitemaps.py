from mininews.sitemaps import MininewsSitemap

from .models import Article


class NewsSitemap(MininewsSitemap):
    model = Article
