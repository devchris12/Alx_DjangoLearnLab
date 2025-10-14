# Django Models Project

This Django project demonstrates advanced model relationships, authentication, role-based access control, and custom permissions.

## Setup Instructions

1. **Create a virtual environment:**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

2. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run migrations:**
   \`\`\`bash
   python manage.py makemigrations relationship_app
   python manage.py migrate
   \`\`\`

4. **Create a superuser:**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

5. **Run the development server:**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

## Features Implemented

### Task 0: Advanced Model Relationships
- **Author Model**: Stores author information
- **Book Model**: ForeignKey relationship to Author
- **Library Model**: ManyToMany relationship to Book
- **Librarian Model**: OneToOne relationship to Library
- **Query Samples**: Sample queries in `query_samples.py`

### Task 1: Views and URL Configuration
- Function-based view for listing books
- Class-based view for library details
- URL patterns configured in `urls.py`
- Templates for displaying data

### Task 2: User Authentication
- Login, logout, and registration views
- Authentication templates
- User session management

### Task 3: Role-Based Access Control
- UserProfile model with role field (Admin, Librarian, Member)
- Role-specific views with access restrictions
- Automatic profile creation using Django signals

### Task 4: Custom Permissions
- Custom permissions on Book model (can_add_book, can_change_book, can_delete_book)
- Permission-protected views for book operations
- Permission enforcement using decorators

## Testing the Application

### Test Queries (Django Shell)
\`\`\`python
python manage.py shell

from relationship_app.query_samples import *

# Query books by author
query_books_by_author("Author Name")

# List books in library
list_books_in_library("Library Name")

# Get librarian for library
retrieve_librarian_for_library("Library Name")
\`\`\`

### Access URLs
- Books list: http://localhost:8000/books/
- Library detail: http://localhost:8000/library/1/
- Login: http://localhost:8000/login/
- Register: http://localhost:8000/register/
- Admin view: http://localhost:8000/admin/
- Librarian view: http://localhost:8000/librarian/
- Member view: http://localhost:8000/member/

## Project Structure
\`\`\`
django-models/
├── django_models/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── relationship_app/       # Main application
│   ├── models.py          # All models defined here
│   ├── views.py           # All views (function and class-based)
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   ├── query_samples.py   # Sample database queries
│   └── templates/         # HTML templates
├── manage.py
└── requirements.txt
