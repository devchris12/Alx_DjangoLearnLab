# Testing Guide

This guide explains how to run and understand the test suite for the Advanced API Project.

## Running Tests

### Run All Tests
\`\`\`bash
python manage.py test api
\`\`\`

### Run Specific Test Class
\`\`\`bash
python manage.py test api.test_views.BookAPITestCase
\`\`\`

### Run Specific Test Method
\`\`\`bash
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
\`\`\`

### Run with Verbose Output
\`\`\`bash
python manage.py test api --verbosity=2
\`\`\`

### Run with Coverage (requires coverage package)
\`\`\`bash
pip install coverage
coverage run --source='api' manage.py test api
coverage report
coverage html  # Generate HTML report
\`\`\`

## Test Structure

### BookAPITestCase
Tests for Book API endpoints covering:

**List Tests**
- `test_get_all_books` - Retrieve all books
- `test_get_books_pagination` - Pagination functionality

**Detail Tests**
- `test_get_book_detail` - Retrieve specific book
- `test_get_nonexistent_book` - 404 handling

**Create Tests**
- `test_create_book_authenticated` - Create with auth
- `test_create_book_unauthenticated` - Permission denied
- `test_create_book_invalid_year` - Validation error
- `test_create_book_missing_fields` - Required fields

**Update Tests**
- `test_update_book_authenticated` - Full update (PUT)
- `test_partial_update_book` - Partial update (PATCH)
- `test_update_book_unauthenticated` - Permission denied

**Delete Tests**
- `test_delete_book_authenticated` - Delete with auth
- `test_delete_book_unauthenticated` - Permission denied

**Filtering Tests**
- `test_filter_books_by_author` - Filter by author ID
- `test_filter_books_by_publication_year` - Exact year match
- `test_filter_books_by_year_range` - Year range filter
- `test_filter_books_by_title_contains` - Partial title match
- `test_filter_books_by_author_name` - Author name filter

**Searching Tests**
- `test_search_books` - Search by title
- `test_search_books_by_author` - Search by author name
- `test_search_no_results` - Empty search results

**Ordering Tests**
- `test_order_books_by_title_ascending` - Sort A-Z
- `test_order_books_by_year_descending` - Sort newest first
- `test_order_books_by_year_ascending` - Sort oldest first

**Combined Tests**
- `test_combined_filter_search_order` - Multiple query params

### AuthorAPITestCase
Tests for Author API endpoints covering:

**List Tests**
- `test_get_all_authors` - Retrieve all authors
- `test_author_includes_books` - Nested book serialization

**Detail Tests**
- `test_get_author_detail` - Retrieve specific author

**Create Tests**
- `test_create_author_authenticated` - Create with auth
- `test_create_author_unauthenticated` - Permission denied

**Update Tests**
- `test_update_author_authenticated` - Update with auth

**Delete Tests**
- `test_delete_author_authenticated` - Delete with auth
- `test_delete_author_cascades_books` - Cascade deletion

**Filtering Tests**
- `test_filter_authors_with_books` - Authors with books
- `test_filter_authors_without_books` - Authors without books
- `test_filter_authors_by_name_contains` - Partial name match

**Searching Tests**
- `test_search_authors` - Search by name

**Ordering Tests**
- `test_order_authors_by_name` - Alphabetical sorting

### SerializerValidationTestCase
Tests for custom validation logic:

- `test_book_serializer_future_year_validation` - Reject future years
- `test_book_serializer_valid_data` - Accept valid data
- `test_book_serializer_unrealistic_year` - Reject unrealistic years

## Test Coverage

The test suite covers:

1. **CRUD Operations** - All create, read, update, delete operations
2. **Authentication** - Permission enforcement for write operations
3. **Validation** - Custom validation rules and error handling
4. **Filtering** - All filter types (exact, range, partial match)
5. **Searching** - Full-text search functionality
6. **Ordering** - Ascending and descending sorts
7. **Edge Cases** - 404 errors, missing fields, invalid data
8. **Data Integrity** - Cascade deletions, nested serialization

## Expected Results

All tests should pass with output similar to:

\`\`\`
Ran 45 tests in 2.345s

OK
\`\`\`

## Troubleshooting

### Tests Fail Due to Database
If tests fail with database errors, ensure migrations are up to date:
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### Import Errors
Ensure all dependencies are installed:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Authentication Errors
The tests use `force_authenticate()` which doesn't require actual tokens.
If you see authentication errors, check that the test setup is creating users correctly.

## Adding New Tests

When adding new features, follow this pattern:

\`\`\`python
def test_new_feature(self):
    """Test description."""
    # Arrange: Set up test data
    data = {...}
    
    # Act: Perform the action
    response = self.client.get(url, data)
    
    # Assert: Verify the results
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('expected_field', response.data)
\`\`\`

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Example GitHub Actions workflow:

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
          python manage.py test api
\`\`\`
