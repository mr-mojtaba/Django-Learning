from django.urls import path
from . import views
from .views import create_post

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),

    # Path definition for functional views
    # path('posts/', views.post_list, name='post_list'),
    path('posts/<int:id>', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/comment', views.post_comment, name='post_comment'),
    path('ticket', views.ticket, name='ticket'),
    path('create_post/', create_post, name='create_post'),

    # Path definition for class-based views
    path('posts/', views.PostListView.as_view(), name='post_list'),
    # path('posts/<pk>', views.PostDetailView.as_view(), name='post_detail'),
]
