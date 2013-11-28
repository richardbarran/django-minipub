from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from mininews.sitemaps import MininewsSitemap

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^mininews/', include('mininews.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="homepage.html"), name='homepage'),
)

urlpatterns += patterns(
    '',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'mininews': MininewsSitemap}}),
)
