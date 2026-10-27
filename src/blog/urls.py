from django.urls import path

from . import api
from . import views

app_name = 'blog'

urlpatterns = [
    path('api/articulos/', api.ArticleListCreateAPIView.as_view(), name='api_articles'),
    path(
        'api/articulos/<int:pk>/',
        api.ArticleDetailAPIView.as_view(),
        name='api_article_detail',
    ),
    path('', views.home, name='home'),
    path('sobre-mi/', views.about, name='about'),
    path('articulos/<slug:slug>/', views.article_detail, name='article_detail'),
]
