from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with token generation
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'bio', 'profile_picture', 'token')
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        user.token = token.key
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile display
    """
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'bio', 'profile_picture',
            'followers_count', 'following_count', 'is_following',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False


class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for nested representations
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture')
