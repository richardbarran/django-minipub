from django.urls import include, path
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from news.sitemaps import NewsSitemap
from news_with_archive.sitemaps import NewsPublishedSitemap, NewsArchivedSitemap

admin.autodiscover()

urlpatterns = [
    path('news/', include('news.urls', namespace='news')),
    path('news_with_archive/',
         include('news_with_archive.urls', namespace='news_with_archive')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(
        template_name="homepage.html"), name='homepage'),
]

urlpatterns += [
    path('sitemap.xml', sitemap,
         {'sitemaps': {'news': NewsSitemap,
                       'published': NewsPublishedSitemap,
                       'archived': NewsArchivedSitemap}})
]
