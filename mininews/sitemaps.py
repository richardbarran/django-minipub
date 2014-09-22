from django.contrib.sitemaps import Sitemap


class MininewsSitemap(Sitemap):

    def items(self):
        return self.model.objects.live()

    def lastmod(self, obj):
        return obj.modified
