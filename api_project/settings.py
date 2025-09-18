import os
# Build paths inside the project (assuming this file is in <project_name>/settings.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# **Security Key & Debug** (Required settings)
SECRET_KEY = 'replace_this_with_a_random_secret_key'  # Django requires a secret key
DEBUG = True                      # True for development (False in production)
ALLOWED_HOSTS = []                # e.g. ['localhost', '127.0.0.1'] when DEBUG is False

# **Installed Applications**
INSTALLED_APPS = [
    # Default Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party and local apps:
    'rest_framework',   # Django REST framework app (DRF) :contentReference[oaicite:5]{index=5}
    'api',              # Your Django app named "api" :contentReference[oaicite:6]{index=6}
]

# **Middleware Configuration** (use Django’s defaults for a basic setup)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# **Root URLs and WSGI/ASGI**
ROOT_URLCONF = '<project_name>.urls'        # Update <project_name> to your project’s name
WSGI_APPLICATION = '<project_name>.wsgi.application'
# ASGI_APPLICATION = '<project_name>.asgi.application'  # If using ASGI

# **Templates Configuration** (needed for admin and DRF’s browsable API)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # You can add template directories here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# **Database Configuration** (using SQLite for development by default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# (You can include additional settings like AUTH_PASSWORD_VALIDATORS, Internationalization,
# Static files config, etc., or rely on Django’s defaults for those in a simple setup.)
