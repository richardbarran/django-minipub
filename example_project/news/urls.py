from django.conf.urls import url
from .views import ArticleDetailView, ArticleArchiveView, ArticleYearArchiveView

app_name = 'news'
urlpatterns = [
    url(r'^$',
        ArticleArchiveView.as_view(),
        name='article_archive'),
    url(r'^year/(?P<year>\d{4})/$',
        ArticleYearArchiveView.as_view(),
        name="article_year"),
    url(r'^(?P<slug>[\w-]+)/$',
        ArticleDetailView.as_view(),
        name='article_detail'),
]
