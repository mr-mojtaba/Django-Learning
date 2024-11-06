from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),

    # Path definition for functional views
    # path('posts/', views.post_list, name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('ticket/', views.ticket, name='ticket'),
    path('search/', views.post_search, name='post_search'),
    path('profile/', views.profile, name='profile'),
    path('profile/create_post/', views.create_post, name='create_post'),
    path('profile/edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('profile/delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('profile/delete_image/<int:post_id>/<int:image_id>/', views.delete_image, name='delete_image'),
    # path('login/', views.user_login, name='user_login'),

    # Path definition for class-based views
    path('posts/', views.PostListView.as_view(), name='post_list'),
    # path('posts/<pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_forme.html' ,success_url='done'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
