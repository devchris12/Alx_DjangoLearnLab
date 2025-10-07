from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser with additional fields
    for social media functionality.
    """
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def follow(self, user):
        """Follow another user"""
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        """Unfollow a user"""
        self.following.remove(user)

    def is_following(self, user):
        """Check if this user is following another user"""
        return self.following.filter(pk=user.pk).exists()
