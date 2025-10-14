from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model
    """
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'comments', 'is_liked'
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
