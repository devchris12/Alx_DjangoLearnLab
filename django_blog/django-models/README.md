# Django Models - Advanced Relationships Project

This Django project demonstrates advanced model relationships, authentication, role-based access control, and custom permissions.

## Project Structure

\`\`\`
django-models/
└── relationship_app/
    ├── models.py              # All models with relationships
    ├── views.py               # Function and class-based views
    ├── urls.py                # URL configuration
    ├── admin.py               # Admin interface configuration
    ├── apps.py                # App configuration
    ├── query_samples.py       # Sample database queries
    └── templates/
        └── relationship_app/
            ├── list_books.html
            ├── library_detail.html
            ├── login.html
            ├── logout.html
            ├── register.html
            ├── admin_view.html
            ├── librarian_view.html
            ├── member_view.html
            ├── add_book.html
            ├── edit_book.html
            └── delete_book.html
\`\`\`

## Setup Instructions

### 1. Create the Django Project (if not already created)

\`\`\`bash
django-admin startproject django_models_project
cd django_models_project
\`\`\`

### 2. Create the relationship_app

\`\`\`bash
python manage.py startapp relationship_app
\`\`\`

### 3. Add the app to INSTALLED_APPS

In your `settings.py`, add:

\`\`\`python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'relationship_app',  # Add this line
]
\`\`\`

### 4. Include the app URLs

In your main `urls.py`, add:

\`\`\`python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
]
\`\`\`

### 5. Run Migrations

\`\`\`bash
python manage.py makemigrations relationship_app
python manage.py migrate
\`\`\`

### 6. Create a Superuser

\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 7. Run the Development Server

\`\`\`bash
python manage.py runserver
\`\`\`

## Features Implemented

### Task 0: Advanced Model Relationships
- **Author Model**: Basic model with CharField
- **Book Model**: ForeignKey relationship to Author
- **Library Model**: ManyToManyField relationship to Book
- **Librarian Model**: OneToOneField relationship to Library
- **Query Samples**: Sample queries demonstrating relationship traversal

### Task 1: Views and URL Configuration
- **Function-based View**: `list_books()` displays all books
- **Class-based View**: `LibraryDetailView` shows library details
- **URL Patterns**: Configured routes for both view types
- **Templates**: HTML templates for rendering data

### Task 2: User Authentication
- **Registration**: User signup with automatic profile creation
- **Login**: User authentication with session management
- **Logout**: User logout functionality
- **Templates**: Complete authentication UI

### Task 3: Role-Based Access Control
- **UserProfile Model**: Extended user model with role field
- **Roles**: Admin, Librarian, Member
- **Signal Handlers**: Automatic profile creation on user registration
- **Role-based Views**: Separate views for each role with access restrictions
- **Decorators**: `@user_passes_test` for role verification

### Task 4: Custom Permissions
- **Custom Permissions**: `can_add_book`, `can_change_book`, `can_delete_book`
- **Permission-based Views**: Views protected by custom permissions
- **Decorators**: `@permission_required` for permission checks

## URL Patterns

- `/books/` - List all books
- `/library/<id>/` - Library detail view
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/admin/` - Admin dashboard (Admin role only)
- `/librarian/` - Librarian dashboard (Librarian role only)
- `/member/` - Member dashboard (Member role only)
- `/books/add/` - Add book (requires can_add_book permission)
- `/books/<id>/edit/` - Edit book (requires can_change_book permission)
- `/books/<id>/delete/` - Delete book (requires can_delete_book permission)

## Testing the Application

### 1. Create Sample Data

Use Django shell to create sample data:

\`\`\`bash
python manage.py shell
\`\`\`

\`\`\`python
from relationship_app.models import Author, Book, Library, Librarian

# Create authors
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George Orwell")

# Create books
book1 = Book.objects.create(title="Harry Potter", author=author1, publication_year=1997)
book2 = Book.objects.create(title="1984", author=author2, publication_year=1949)

# Create library
library = Library.objects.create(name="Central Library")
library.books.add(book1, book2)

# Create librarian
librarian = Librarian.objects.create(name="John Doe", library=library)
\`\`\`

### 2. Test Queries

\`\`\`bash
python manage.py shell
\`\`\`

\`\`\`python
from relationship_app.query_samples import *

# Test queries
query_books_by_author("J.K. Rowling")
list_books_in_library("Central Library")
retrieve_librarian_for_library("Central Library")
\`\`\`

### 3. Assign Roles and Permissions

In Django admin (`/admin/`):
1. Create users
2. Assign roles via UserProfile
3. Assign custom permissions via User permissions

## Models Overview

### Author
- `name`: CharField - Author's name

### Book
- `title`: CharField - Book title
- `author`: ForeignKey - Reference to Author
- `publication_year`: IntegerField - Year of publication
- Custom permissions: can_add_book, can_change_book, can_delete_book

### Library
- `name`: CharField - Library name
- `books`: ManyToManyField - Books in the library

### Librarian
- `name`: CharField - Librarian's name
- `library`: OneToOneField - Associated library

### UserProfile
- `user`: OneToOneField - Reference to Django User
- `role`: CharField - User role (Admin/Librarian/Member)

## Security Features

- CSRF protection on all forms
- Login required decorators
- Role-based access control
- Custom permission checks
- Automatic user profile creation

## Notes

- All templates include basic styling for better presentation
- Signal handlers automatically create UserProfile when users register
- Permission checks raise exceptions for unauthorized access
- Role checks redirect to login page for unauthenticated users
