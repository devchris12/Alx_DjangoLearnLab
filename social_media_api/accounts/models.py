from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    User profile model with following/followers functionality.
    
    TASK: Develop views in the accounts app that allow users to follow and unfollow others
    - ManyToManyField 'following' tracks users that this profile follows
    - Related name 'followers' allows reverse lookup of who follows this user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def follow(self, profile):
        """Follow another user's profile"""
        self.following.add(profile)
    
    def unfollow(self, profile):
        """Unfollow another user's profile"""
        self.following.remove(profile)
    
    def is_following(self, profile):
        """Check if this profile is following another profile"""
        return self.following.filter(pk=profile.pk).exists()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a new user is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile when the user is saved"""
    instance.profile.save()
    from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # A user can follow many other users, and be followed by others
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username

