from django.conf.urls import patterns, url
from .views import ArticleDetailView, ArticleArchiveView

urlpatterns = patterns('',
                       url(r'^$',
                           ArticleArchiveView.as_view(),
                           name='article_archive'),
                       url(r'^(?P<slug>[\w-]+)/$',
                           ArticleDetailView.as_view(),
                           name='article_detail'),
                       )
