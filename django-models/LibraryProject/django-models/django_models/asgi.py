"""
ASGI config for django_models project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')

application = get_asgi_application()
