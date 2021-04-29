from django.urls import path
from .views import ArticleDetailView, ArticleArchiveView, ArticleArchivedArchiveView, \
    ArticleArchivedDetailView

app_name = 'news_with_archive'
urlpatterns = [
    path('news/',
         ArticleArchiveView.as_view(),
         name='article_archive'),
    path('news/<slug:slug>/',
         ArticleDetailView.as_view(),
         name='article_detail'),
    path('archived/',
         ArticleArchivedArchiveView.as_view(),
         name='article_archived_archive'),
    path('archived/<slug:slug>/',
         ArticleArchivedDetailView.as_view(),
         name='article_archived_detail'),
]
