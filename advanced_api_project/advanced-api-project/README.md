# Advanced API Project - Django REST Framework

This project is part of the Alx_DjangoLearnLab repository and focuses on building an advanced API using Django REST Framework with custom serializers, views, filtering, and comprehensive testing.

## Project Overview

This tutorial covers four main tasks:
1. Setting up Django with custom serializers
2. Building custom and generic views
3. Implementing filtering, searching, and ordering
4. Writing comprehensive unit tests

---

## Task 0: Setting Up a New Django Project with Custom Serializers

**Status:** 0.0% Complete

### Objective
Initiate a new Django project tailored for advanced API development with Django REST Framework, focusing on creating custom serializers that handle complex data structures and nested relationships.

### Step 1: Install Django and Django REST Framework
- Install Django and Django REST Framework using pip
- Create a new Django project named `advanced-api-project` using: `django-admin startproject advanced-api-project .`
- Create a new Django app named `api`

### Step 2: Configure the Project
- Add `rest_framework` to `INSTALLED_APPS` in `settings.py`
- Use Django's default SQLite database for simplicity

### Step 3: Define Data Models
Create two models in `api/models.py`:

**Author Model:**
- `name`: string field for the author's name

**Book Model:**
- `title`: string field for the book's title
- `publication_year`: integer field for the year published
- `author`: foreign key linking to Author (one-to-many relationship)

Run migrations to create these models in the database.

### Step 4: Create Custom Serializers
- Create a `BookSerializer` that serializes all fields of the Book model
- Create an `AuthorSerializer` that includes:
  - The `name` field
  - A nested `BookSerializer` to serialize related books dynamically
- Add custom validation to `BookSerializer` to ensure `publication_year` is not in the future

### Step 5: Document Your Model and Serializer Setup
- Add detailed comments in `models.py` and `serializers.py`
- Describe how the Author-Book relationship is handled in serializers

### Step 6: Implement and Test
- Use Django admin or Django shell to test creating, retrieving, and serializing Author and Book instances

---

## Task 1: Building Custom Views and Generic Views

**Status:** 0.0% Complete

### Objective
Learn to construct custom views and utilize generic views in Django REST Framework to handle specific use cases and streamline API development.

### Step 1: Set Up Generic Views
Implement generic views for the Book model:
- `ListView` for retrieving all books
- `DetailView` for retrieving a single book by ID
- `CreateView` for adding a new book
- `UpdateView` for modifying an existing book
- `DeleteView` for removing a book

### Step 2: Define URL Patterns
Configure URL patterns in `api/urls.py`:
- `/books/` for the list view
- `/books/<int:pk>/` for the detail view
- Appropriate URLs for create, update, and delete operations

### Step 3: Customize View Behavior
- Customize `CreateView` and `UpdateView` for proper form submissions and validation
- Integrate permission checks or filters using DRF's built-in features

### Step 4: Implement Permissions
- Apply Django REST Framework's permission classes
- Restrict `CreateView`, `UpdateView`, and `DeleteView` to authenticated users only
- Allow read-only access for unauthenticated users on `ListView` and `DetailView`

### Step 5: Test the Views
- Test each view using Postman or curl
- Verify CRUD operations work correctly
- Confirm permissions are enforced properly

### Step 6: Document the View Configurations
- Provide clear documentation via code comments
- Create external README detailing view configurations
- Outline custom settings or hooks used

---

## Task 2: Implementing Filtering, Searching, and Ordering

**Status:** 0.0% Complete

### Objective
Enhance API usability by implementing filtering, searching, and ordering capabilities.

### Step 1: Set Up Filtering
- Integrate Django REST Framework's filtering capabilities
- Allow users to filter book list by `title`, `author`, and `publication_year`
- Use DRF's `DjangoFilterBackend` in your `ListView`

### Step 2: Implement Search Functionality
- Enable search on `title` and `author` fields
- Configure `SearchFilter` in your API

### Step 3: Configure Ordering
- Allow users to order results by any field, particularly `title` and `publication_year`
- Set up `OrderingFilter` for front-end flexibility

### Step 4: Update API Views
- Adjust `BookListView` to incorporate filtering, searching, and ordering
- Ensure capabilities are clearly defined in view logic

### Step 5: Test API Functionality
- Test filtering, searching, and ordering features
- Use Postman or curl with various query parameters

### Step 6: Document the Implementation
- Detail implementation in views
- Include examples of API requests in documentation

---

## Task 3: Writing Unit Tests for Django REST Framework APIs

**Status:** 0.0% Complete

### Objective
Develop and execute comprehensive unit tests for your Django REST Framework APIs to ensure endpoint integrity and correctness.

### Step 1: Understand What to Test
Focus on:
- CRUD operations for Book model endpoints
- Filtering, searching, and ordering functionalities
- Permissions and authentication mechanisms

### Step 2: Set Up Testing Environment
- Use Django's built-in test framework (based on Python's unittest)
- Configure a separate test database

### Step 3: Write Test Cases
Write tests in `/api/test_views.py` that:
- Create a Book and verify data is correctly saved and returned
- Update a Book and verify changes are reflected
- Delete a Book and ensure removal from database
- Test each endpoint with appropriate authentication and permission scenarios

### Step 4: Run and Review Tests
Execute tests using:
\`\`\`bash
python manage.py test api
\`\`\`
Review outputs and fix any issues identified.

### Step 5: Document Your Testing Approach
- Document testing strategy and individual test cases
- Provide guidelines on running tests and interpreting results

---

## Repository Information

- **GitHub Repository:** Alx_DjangoLearnLab
- **Directory:** advanced-api-project

---

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install django djangorestframework`
3. Follow the tasks in order
4. Run migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

## Testing

Run all tests with:
\`\`\`bash
python manage.py test api
\`\`\`

## Documentation

Each task includes detailed documentation requirements. Ensure all code is well-commented and includes explanations of:
- Model relationships
- Serializer logic
- View configurations
- Permission settings
- Test scenarios
