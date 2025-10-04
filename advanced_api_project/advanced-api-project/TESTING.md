# Testing Guide

## Running Tests

### Run all tests
\`\`\`bash
python manage.py test
\`\`\`

### Run specific test class
\`\`\`bash
python manage.py test api.tests.AuthorModelTest
python manage.py test api.tests.BookAPITest
\`\`\`

### Run specific test method
\`\`\`bash
python manage.py test api.tests.AuthorAPITest.test_create_author_authenticated
\`\`\`

### Run with verbose output
\`\`\`bash
python manage.py test --verbosity=2
\`\`\`

### Run with coverage (install coverage first: pip install coverage)
\`\`\`bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
\`\`\`

## Test Coverage

The test suite includes comprehensive tests for:

### 1. Model Tests
- **AuthorModelTest**: Tests Author model creation, string representation, and ordering
- **BookModelTest**: Tests Book model creation, relationships, and ordering

### 2. Serializer Tests
- **AuthorSerializerTest**: Tests Author serializer fields and custom validation
  - Name length validation (minimum 2 characters)
  - Name format validation (cannot be only numbers)
- **BookSerializerTest**: Tests Book serializer fields and custom validation
  - ISBN format validation (digits and hyphens only)
  - ISBN length validation (exactly 13 digits)
  - Published date validation (cannot be in future)
  - Number of pages validation (must be positive)

### 3. API Endpoint Tests
- **AuthorAPITest**: Tests Author API endpoints
  - GET list of authors
  - GET single author detail
  - POST create author (authenticated)
  - POST create author (unauthenticated - should fail)
  - PUT update author (authenticated)
  - DELETE author (authenticated)

- **BookAPITest**: Tests Book API endpoints
  - GET list of books
  - GET single book detail
  - POST create book (authenticated)
  - POST create book (unauthenticated - should fail)
  - PUT update book (authenticated)
  - DELETE author (authenticated)

### 4. Filtering, Searching, and Ordering Tests
- **FilteringSearchOrderingTest**: Tests advanced query capabilities
  - Filter books by author name
  - Filter books by publication year
  - Filter books by page count range
  - Search books by title, ISBN, or author name
  - Search authors by name or bio
  - Order books by title (ascending)
  - Order books by published date (descending)
  - Combined filtering, searching, and ordering

### 5. Pagination Tests
- **PaginationTest**: Tests pagination functionality
  - First page returns correct number of items
  - Second page returns remaining items
  - Next/previous links work correctly

## Test Data

The tests use the following test data:

### Authors
- John Doe - "A prolific author of technical books."
- Jane Smith - "An experienced technical writer."

### Books
- Django for Beginners (ISBN: 978-1234567890, 350 pages, 2023-01-15)
- Advanced Django (ISBN: 978-0987654321, 450 pages, 2024-06-20)
- Python Basics (ISBN: 978-1111111111, 250 pages, 2022-03-10)

## Expected Test Results

All tests should pass. Expected output:

\`\`\`
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................................................
----------------------------------------------------------------------
Ran 50 tests in X.XXXs

OK
Destroying test database for alias 'default'...
\`\`\`

## Continuous Integration

To integrate these tests into a CI/CD pipeline:

1. **GitHub Actions Example** (.github/workflows/tests.yml):
\`\`\`yaml
name: Django Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python manage.py test
\`\`\`

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. **Database errors**: Ensure migrations are up to date
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

3. **Permission errors**: Tests create a test database automatically, ensure you have write permissions

## Adding New Tests

When adding new features, follow these guidelines:

1. **Model changes**: Add tests in the appropriate ModelTest class
2. **Serializer changes**: Add tests in the appropriate SerializerTest class
3. **API changes**: Add tests in the appropriate APITest class
4. **New features**: Create a new test class following the existing patterns

Example:
\`\`\`python
class NewFeatureTest(APITestCase):
    def setUp(self):
        # Setup test data
        pass
    
    def test_new_feature(self):
        # Test the new feature
        pass
\`\`\`
