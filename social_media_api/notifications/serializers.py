from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model
    """
    actor = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = (
            'id', 'recipient', 'actor', 'verb', 'target_content_type',
            'target_object_id', 'read', 'timestamp'
        )
        read_only_fields = (
            'id', 'recipient', 'actor', 'verb', 'target_content_type',
            'target_object_id', 'timestamp'
        )
