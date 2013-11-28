from django.conf.urls import patterns, include, url

from .sitemaps import MininewsSitemap

urlpatterns = patterns('',
    (r'^mininews/', include('mininews.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': MininewsSitemap}}),
)

