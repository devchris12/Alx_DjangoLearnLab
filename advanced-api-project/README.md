# Advanced API Project

A Django REST Framework project demonstrating advanced API development concepts including custom serializers, generic views, filtering, searching, ordering, and comprehensive testing.

## Features

- **Custom Serializers**: Nested serializers with custom validation
- **Generic Views**: CRUD operations using DRF's generic views
- **Filtering**: Filter books by title, author, and publication year
- **Searching**: Full-text search on book titles and author names
- **Ordering**: Sort results by any field
- **Permissions**: Role-based access control
- **Unit Tests**: Comprehensive test coverage

## Installation

1. Create a virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Run migrations:
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

4. Create a superuser:
\`\`\`bash
python manage.py createsuperuser
\`\`\`

5. Run the development server:
\`\`\`bash
python manage.py runserver
\`\`\`

## API Endpoints

- `GET /api/books/` - List all books (supports filtering, searching, ordering)
- `GET /api/books/<id>/` - Retrieve a specific book
- `POST /api/books/` - Create a new book (authentication required)
- `PUT /api/books/<id>/` - Update a book (authentication required)
- `DELETE /api/books/<id>/` - Delete a book (authentication required)

## Query Parameters

### Filtering
- `?title=<title>` - Filter by exact title
- `?author=<author_id>` - Filter by author ID
- `?publication_year=<year>` - Filter by publication year

### Searching
- `?search=<query>` - Search in title and author name

### Ordering
- `?ordering=title` - Order by title (ascending)
- `?ordering=-publication_year` - Order by publication year (descending)

## Running Tests

\`\`\`bash
python manage.py test api
\`\`\`

## Project Structure

\`\`\`
advanced-api-project/
├── advanced_api_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── models.py          # Author and Book models
│   ├── serializers.py     # Custom serializers with validation
│   ├── views.py           # Generic views with permissions
│   ├── urls.py            # API routing
│   └── test_views.py      # Unit tests
├── manage.py
└── requirements.txt
