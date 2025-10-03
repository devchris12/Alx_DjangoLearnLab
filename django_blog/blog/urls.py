from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Blog Post URLs
    path('', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Comment URLs - Logically structured and intuitive
    # Example: /posts/int:post_id/comments/new/ for creating a comment
    path('posts/<int:post_id>/comments/new/', views.add_comment, name='add_comment'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # URL Configuration for New Features (Search and Tags)
    path('search/', views.search_posts, name='search'),
    path('tags/<slug:tag_slug>/', views.posts_by_tag, name='posts_by_tag'),
]
