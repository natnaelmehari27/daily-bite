from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('create/', views.create_news_post, name='create_news_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]