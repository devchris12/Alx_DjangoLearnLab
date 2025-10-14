# Signals are imported in models.py, but we can keep this file for organization
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
