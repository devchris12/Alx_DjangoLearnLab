"""
Script to create sample data for testing the Social Media API
Run with: python manage.py shell < scripts/create_sample_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Like
from notifications.models import Notification

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create users
    users = []
    for i in range(1, 6):
        user, created = User.objects.get_or_create(
            username=f'user{i}',
            defaults={
                'email': f'user{i}@example.com',
                'bio': f'I am user {i}. Welcome to my profile!'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {user.username}")
        users.append(user)
    
    # Create follow relationships
    users[0].follow(users[1])
    users[0].follow(users[2])
    users[1].follow(users[0])
    users[2].follow(users[0])
    users[3].follow(users[0])
    print("Created follow relationships")
    
    # Create posts
    posts = []
    post_data = [
        ("Introduction", "Hello everyone! This is my first post on this platform."),
        ("Django Tips", "Just learned about Django signals. They're amazing for decoupling code!"),
        ("REST API Best Practices", "Always use proper HTTP status codes in your API responses."),
        ("Python Programming", "List comprehensions are a powerful feature in Python."),
        ("Web Development", "Responsive design is crucial for modern web applications."),
    ]
    
    for i, (title, content) in enumerate(post_data):
        post = Post.objects.create(
            author=users[i % len(users)],
            title=title,
            content=content
        )
        posts.append(post)
        print(f"Created post: {title}")
    
    # Create comments
    comments_data = [
        (posts[0], users[1], "Welcome! Great to have you here."),
        (posts[0], users[2], "Nice to meet you!"),
        (posts[1], users[0], "Thanks for sharing! Very helpful."),
        (posts[2], users[3], "Totally agree with this approach."),
        (posts[3], users[4], "Python is awesome!"),
    ]
    
    for post, author, content in comments_data:
        Comment.objects.create(
            post=post,
            author=author,
            content=content
        )
    print("Created comments")
    
    # Create likes
    Like.objects.get_or_create(user=users[1], post=posts[0])
    Like.objects.get_or_create(user=users[2], post=posts[0])
    Like.objects.get_or_create(user=users[0], post=posts[1])
    Like.objects.get_or_create(user=users[3], post=posts[2])
    print("Created likes")
    
    print("\nSample data created successfully!")
    print(f"Users: {User.objects.count()}")
    print(f"Posts: {Post.objects.count()}")
    print(f"Comments: {Comment.objects.count()}")
    print(f"Likes: {Like.objects.count()}")
    print(f"Notifications: {Notification.objects.count()}")

if __name__ == '__main__':
    create_sample_data()
