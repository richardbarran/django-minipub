from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from news.sitemaps import NewsSitemap
from news_with_archive.sitemaps import NewsPublishedSitemap, NewsArchivedSitemap

admin.autodiscover()

urlpatterns = [
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^news_with_archive/',
        include('news_with_archive.urls', namespace='news_with_archive')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(
        template_name="homepage.html"), name='homepage'),
]

urlpatterns += [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'news': NewsSitemap,
                      'published': NewsPublishedSitemap,
                      'archived': NewsArchivedSitemap}})
]
