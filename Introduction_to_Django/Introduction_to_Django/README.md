# LibraryProject - Django Development Environment Setup

## Overview
This is a Django project created as part of the ALX Django LearnLab. The project demonstrates the fundamentals of Django development, including project setup, model creation, and admin interface configuration.

## Project Structure
\`\`\`
LibraryProject/
├── manage.py
├── LibraryProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── bookshelf/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── views.py
    └── migrations/
        └── __init__.py
\`\`\`

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Installation Steps

### 1. Install Django
\`\`\`bash
pip install django
\`\`\`

### 2. Create Django Project
The project has already been created with the following command:
\`\`\`bash
django-admin startproject LibraryProject
\`\`\`

### 3. Create the bookshelf App
Navigate to the project directory and create the app:
\`\`\`bash
cd LibraryProject
python manage.py startapp bookshelf
\`\`\`

### 4. Configure the Application
Add 'bookshelf' to INSTALLED_APPS in `LibraryProject/settings.py`:
\`\`\`python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',  # Add this line
]
\`\`\`

### 5. Run Migrations
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 6. Create a Superuser (for Admin Interface)
\`\`\`bash
python manage.py createsuperuser
\`\`\`
Follow the prompts to create an admin account.

### 7. Run the Development Server
\`\`\`bash
python manage.py runserver
\`\`\`

Visit `http://127.0.0.1:8000/` to view the Django welcome page.
Visit `http://127.0.0.1:8000/admin/` to access the admin interface.

## Project Components

### settings.py
Contains all the configuration for the Django project, including:
- Database configuration
- Installed applications
- Middleware settings
- Template configuration
- Static files configuration

### urls.py
The URL declarations for the project - a "table of contents" of your Django-powered site. It maps URL patterns to views.

### manage.py
A command-line utility that lets you interact with this Django project in various ways:
- `runserver`: Start the development server
- `makemigrations`: Create new migrations based on model changes
- `migrate`: Apply migrations to the database
- `createsuperuser`: Create an admin user
- `shell`: Open a Python shell with Django environment loaded

## Book Model
The `bookshelf` app includes a Book model with the following fields:
- **title**: CharField (max 200 characters)
- **author**: CharField (max 100 characters)
- **publication_year**: IntegerField

## CRUD Operations
See the following files for detailed CRUD operation examples:
- `create.md` - Creating book instances
- `retrieve.md` - Retrieving book data
- `update.md` - Updating book information
- `delete.md` - Deleting book instances

## Admin Interface
The Book model is registered with the Django admin interface with custom configurations:
- List display shows title, author, and publication year
- Search functionality for title and author
- Filter by publication year

## Repository Information
- **GitHub Repository**: Alx_DjangoLearnLab
- **Directory**: Introduction_to_Django

## Learning Objectives
1. ✅ Set up a Django development environment
2. ✅ Create a Django project and app
3. ✅ Define models with appropriate field types
4. ✅ Perform database migrations
5. ✅ Execute CRUD operations using Django ORM
6. ✅ Configure and customize the Django admin interface

## Next Steps
- Explore Django views and templates
- Learn about URL routing
- Implement forms and user input validation
- Add authentication and authorization
