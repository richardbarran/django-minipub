from django.conf.urls import patterns, url
from .views import ArticleDetailView, ArticleArchiveView, ArticleYearArchiveView

urlpatterns = patterns('',
                       url(r'^$',
                           ArticleArchiveView.as_view(),
                           name='article_archive'),
                       url(r'^year/(?P<year>\d{4})/$',
                           ArticleYearArchiveView.as_view(),
                           name="article_year"),
                       url(r'^(?P<slug>[\w-]+)/$',
                           ArticleDetailView.as_view(),
                           name='article_detail'),
                       )
