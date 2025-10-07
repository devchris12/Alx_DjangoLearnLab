from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model with CRUD operations
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """
        Get posts from users that the current user follows
        """
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users)
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        Like a post
        """
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            return Response({
                'message': 'Post liked successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'You have already liked this post'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        Unlike a post
        """
        post = self.get_object()
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({
                'message': 'Post unliked successfully'
            }, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({
                'error': 'You have not liked this post'
            }, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model with CRUD operations
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
        from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class FeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        # Get all the users the current user follows
        following_users = request.user.following.all()

        # Filter posts from followed users, newest first
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Serialize and return them
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Like, Notification

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user

        # Check if already liked
        if Like.objects.filter(user=user, post=post).exists():
            return Response({"message": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create like
        Like.objects.create(user=user, post=post)

        # Create notification
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                sender=user,
                post=post,
                message=f"{user.username} liked your post."
            )

        return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user

        # Check if not liked yet
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({"message": "You haven’t liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)
