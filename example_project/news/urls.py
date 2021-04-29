from django.urls import path
from .views import ArticleDetailView, ArticleArchiveView, ArticleYearArchiveView

app_name = 'news'
urlpatterns = [
    path('',
         ArticleArchiveView.as_view(),
         name='article_archive'),
    path('year/<int:year>/',
         ArticleYearArchiveView.as_view(),
         name="article_year"),
    path('<slug:slug>/',
         ArticleDetailView.as_view(),
         name='article_detail'),
]
