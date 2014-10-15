from django.conf.urls import patterns, url
from .views import ArticleDetailView, ArticleArchiveView, ArticleArchivedArchiveView, \
    ArticleArchivedDetailView

urlpatterns = patterns('',
                       url(r'^news/$',
                           ArticleArchiveView.as_view(),
                           name='article_archive'),
                       url(r'^news/(?P<slug>[\w-]+)/$',
                           ArticleDetailView.as_view(),
                           name='article_detail'),
                       url(r'^archived/$',
                           ArticleArchivedArchiveView.as_view(),
                           name='article_archived_archive'),
                       url(r'^archived/(?P<slug>[\w-]+)/$',
                           ArticleArchivedDetailView.as_view(),
                           name='article_archived_detail'),
                       )
