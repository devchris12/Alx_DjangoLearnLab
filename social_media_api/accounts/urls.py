from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserDetailView,
    FollowUserView,
    UnfollowUserView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # TASK: Set up URL patterns in accounts/urls.py for follow management
    # Follow/unfollow URLs with user_id parameter
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
]

