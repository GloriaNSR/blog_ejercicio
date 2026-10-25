from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre-mi/', views.about, name='about'),
    path('articulos/<slug:slug>/', views.article_detail, name='article_detail'),
]
