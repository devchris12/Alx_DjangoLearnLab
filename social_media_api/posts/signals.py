from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Comment
from notifications.models import Notification


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """
    Create a notification when a post is liked
    """
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.user,
            verb='liked your post',
            target_content_type_id=instance.post.pk,
            target_object_id=instance.post.pk
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    Create a notification when a comment is made
    """
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.author,
            verb='commented on your post',
            target_content_type_id=instance.post.pk,
            target_object_id=instance.post.pk
        )
