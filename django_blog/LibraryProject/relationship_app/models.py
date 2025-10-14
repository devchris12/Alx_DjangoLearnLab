from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    """Author model with a name field"""
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """Book model with title and ForeignKey to Author"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    class Meta:
        permissions = [
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        ]
    
    def __str__(self):
        return self.title

class Library(models.Model):
    """Library model with name and ManyToMany relationship to Book"""
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name

class Librarian(models.Model):
    """Librarian model with OneToOne relationship to Library"""
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """UserProfile model extending User with role-based access"""
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Signal to automatically create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

from django.db import models

class Author(models.Model):
    """Author model with a name field"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        from django.db import models


class Author(models.Model):
    """Model representing a book author."""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """Model representing a book in the library."""
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']

