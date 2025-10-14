# LibraryProject - Django Models and Views

A comprehensive Django application demonstrating advanced model relationships, authentication, role-based access control, and custom permissions.

## Features

### Task 0: Advanced Model Relationships
- **Author Model**: Basic model with name field
- **Book Model**: ForeignKey relationship to Author
- **Library Model**: ManyToMany relationship to Book
- **Librarian Model**: OneToOne relationship to Library
- **Query Samples**: Pre-built queries for common operations

### Task 1: Views and URL Configuration
- **Function-based View**: `list_books` - Lists all books with authors
- **Class-based View**: `LibraryDetailView` - Shows library details
- **URL Routing**: Complete URL configuration for all views

### Task 2: User Authentication
- User registration with automatic profile creation
- Login and logout functionality
- Session management

### Task 3: Role-Based Access Control
- **UserProfile Model**: Extends User with Admin/Librarian/Member roles
- **Role-specific Views**: Separate views for each role
- **Automatic Profile Creation**: Django signals create profiles on user registration

### Task 4: Custom Permissions
- `can_add_book`: Permission to add books
- `can_change_book`: Permission to edit books
- `can_delete_book`: Permission to delete books
- Permission-protected views for book management

## Setup Instructions

### 1. Install Django
\`\`\`bash
pip install django
\`\`\`

### 2. Create the Project (if not already created)
\`\`\`bash
django-admin startproject LibraryProject
cd LibraryProject
\`\`\`

### 3. Create the App
\`\`\`bash
python manage.py startapp relationship_app
\`\`\`

### 4. Configure Settings
Add to `LibraryProject/settings.py`:
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

### 5. Configure URLs
Update `LibraryProject/urls.py`:
\`\`\`python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
]
\`\`\`

### 6. Run Migrations
\`\`\`bash
python manage.py makemigrations relationship_app
python manage.py migrate
\`\`\`

### 7. Create Superuser
\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 8. Run the Server
\`\`\`bash
python manage.py runserver
\`\`\`

## Testing the Application

### 1. Create Test Data
\`\`\`bash
python manage.py shell
\`\`\`

\`\`\`python
from relationship_app.models import Author, Book, Library, Librarian

# Create authors
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George Orwell")

# Create books
book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
book3 = Book.objects.create(title="1984", author=author2)

# Create library
library = Library.objects.create(name="Central Library")
library.books.add(book1, book2, book3)

# Create librarian
librarian = Librarian.objects.create(name="John Doe", library=library)
\`\`\`

### 2. Test Query Samples
\`\`\`python
from relationship_app.query_samples import *

# Query all books by a specific author
books = query_books_by_author("J.K. Rowling")
for book in books:
    print(book.title)

# List all books in a library
books = list_books_in_library("Central Library")
for book in books:
    print(book.title)

# Retrieve the librarian for a library
librarian = retrieve_librarian_for_library("Central Library")
print(librarian.name)
\`\`\`

### 3. Access Views
- Books List: http://127.0.0.1:8000/books/
- Library Detail: http://127.0.0.1:8000/library/1/
- Register: http://127.0.0.1:8000/register/
- Login: http://127.0.0.1:8000/login/
- Admin View: http://127.0.0.1:8000/admin/
- Librarian View: http://127.0.0.1:8000/librarian/
- Member View: http://127.0.0.1:8000/member/

### 4. Assign Permissions
In Django admin or shell:
\`\`\`python
from django.contrib.auth.models import User, Permission

user = User.objects.get(username='your_username')
user.user_permissions.add(
    Permission.objects.get(codename='can_add_book'),
    Permission.objects.get(codename='can_change_book'),
    Permission.objects.get(codename='can_delete_book')
)
\`\`\`

### 5. Set User Roles
\`\`\`python
from relationship_app.models import UserProfile

profile = user.userprofile
profile.role = 'Admin'  # or 'Librarian' or 'Member'
profile.save()
\`\`\`

## Project Structure
\`\`\`
LibraryProject/
├── LibraryProject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── relationship_app/
│   ├── migrations/
│   ├── templates/
│   │   └── relationship_app/
│   │       ├── list_books.html
│   │       ├── library_detail.html
│   │       ├── login.html
│   │       ├── logout.html
│   │       ├── register.html
│   │       ├── admin_view.html
│   │       ├── librarian_view.html
│   │       ├── member_view.html
│   │       ├── add_book.html
│   │       ├── edit_book.html
│   │       └── delete_book.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── query_samples.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
└── manage.py
\`\`\`

## Key Concepts Demonstrated

1. **Model Relationships**:
   - ForeignKey (Book → Author)
   - ManyToMany (Library ↔ Book)
   - OneToOne (Librarian → Library)

2. **Views**:
   - Function-based views
   - Class-based views (DetailView)

3. **Authentication**:
   - User registration
   - Login/logout
   - Session management

4. **Authorization**:
   - Role-based access control
   - Custom permissions
   - Permission decorators

5. **Django Signals**:
   - Automatic UserProfile creation

## Troubleshooting

### Issue: Templates not found
Make sure your `TEMPLATES` setting in `settings.py` includes:
\`\`\`python
'APP_DIRS': True,
\`\`\`

### Issue: Permissions not working
Run migrations after adding custom permissions:
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### Issue: UserProfile not created
The signal should create it automatically. If not, create manually:
\`\`\`python
from relationship_app.models import UserProfile
UserProfile.objects.create(user=user, role='Member')
