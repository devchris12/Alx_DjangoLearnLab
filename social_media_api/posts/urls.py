from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

app_name = 'posts'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('feed/', PostViewSet.as_view({'get': 'feed'}), name='feed'),
    path('', include(router.urls)),
]
from django.urls import path
from .views import LikePostView, UnlikePostView

urlpatterns = [
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]
