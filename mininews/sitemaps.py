'''
.. _sitemaps-label:

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

If you have custom statuses...
------------------------------
If you have more statuses than the default 'draft', 'published', and you have different
sets of views to display these - you will also need extra sitemap classes.

You can add a ``mininews_live`` attribute to your sitemap class - exactly
the same way as you will have done for your extra views. For example:

.. code-block:: python

    from mininews.sitemaps import MininewsSitemap

    from .models import Article

    class NewsArchivesSitemap(MininewsSitemap):
        """Sitemap for the archived articles."""
        model = Article
        mininews_live = ('archived',)

'''
from django.contrib.sitemaps import Sitemap


class MininewsSitemap(Sitemap):

    mininews_live = ('published',)

    def items(self):
        return self.model.objects.live(statuses=self.mininews_live)

    def lastmod(self, obj):
        return obj.modified
