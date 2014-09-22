"""
We have a ``MininewsSitemap`` class that provides a small amount of boilerplate
to make creating a sitemap easier.

Here is an example of how to use it:

.. code-block:: python
    
    from mininews.sitemaps import MininewsSitemap
    
    from .models import Article
    
    class NewsSitemap(MininewsSitemap):
        model = Article

Basically, all you'll need to do is set the model to use in the sitemap - in 
this example, it's ``Article``.
"""
from django.contrib.sitemaps import Sitemap


class MininewsSitemap(Sitemap):

    def items(self):
        return self.model.objects.live()

    def lastmod(self, obj):
        return obj.modified
