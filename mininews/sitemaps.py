from django.contrib.sitemaps import Sitemap

class MininewsSitemap(Sitemap):

    # Let's assume that an article - once published - will not change.
    changefreq = "never"

    # Define the model class here to make it easier to customise this class.
    model = None

    def items(self):
        return self.model.objects.viewable()

    def lastmod(self, obj):
        return obj.modified

    def priority(self, obj):
        return obj.sitemap_priority
