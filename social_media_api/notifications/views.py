from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark a notification as read
        """
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({
            'message': 'Notification marked as read'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Mark all notifications as read
        """
        notifications = self.get_queryset().filter(read=False)
        notifications.update(read=True)
        return Response({
            'message': f'{notifications.count()} notifications marked as read'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """
        Get all unread notifications
        """
        unread_notifications = self.get_queryset().filter(read=False)
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)
