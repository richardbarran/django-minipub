from mininews.sitemaps import MininewsSitemap

from .models import Article

class BlogSitemap(MininewsSitemap):
    model = Article