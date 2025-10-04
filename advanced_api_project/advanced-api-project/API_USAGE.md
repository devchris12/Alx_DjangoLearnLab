# API Usage Guide

## Base URL
\`\`\`
http://localhost:8000/api/
\`\`\`

## Authentication
The API uses session authentication and basic authentication. Most endpoints allow read access without authentication, but write operations require authentication.

## Endpoints

### Authors

#### Function-Based Views (FBV)
- **List/Create Authors**: \`GET/POST /api/fbv/authors/\`
- **Author Detail**: \`GET/PUT/DELETE /api/fbv/authors/{id}/\`

#### Generic Views (Recommended - with filtering)
- **List/Create Authors**: \`GET/POST /api/authors/\`
- **Author Detail**: \`GET/PUT/DELETE /api/authors/{id}/\`

#### ViewSets
- **Authors**: \`/api/viewset-authors/\`

### Books

#### Class-Based Views (CBV)
- **List/Create Books**: \`GET/POST /api/cbv/books/\`
- **Book Detail**: \`GET/PUT/DELETE /api/cbv/books/{id}/\`

#### Generic Views (Recommended - with filtering)
- **List/Create Books**: \`GET/POST /api/books/\`
- **Book Detail**: \`GET/PUT/DELETE /api/books/{id}/\`

#### ViewSets
- **Books**: \`/api/viewset-books/\`

## Filtering, Searching, and Ordering

### Authors

#### Filtering
\`\`\`
GET /api/authors/?name=John
GET /api/authors/?name_exact=John Doe
\`\`\`

#### Searching
\`\`\`
GET /api/authors/?search=John
\`\`\`

#### Ordering
\`\`\`
GET /api/authors/?ordering=name
GET /api/authors/?ordering=-name  # Descending
\`\`\`

### Books

#### Filtering
\`\`\`
# Filter by title (partial match)
GET /api/books/?title=Django

# Filter by author name
GET /api/books/?author_name=John

# Filter by publication year
GET /api/books/?published_year=2023

# Filter by date range
GET /api/books/?published_after=2020-01-01&published_before=2023-12-31

# Filter by page count
GET /api/books/?min_pages=100&max_pages=500

# Filter by exact ISBN
GET /api/books/?isbn=978-1234567890

# Filter by author ID
GET /api/books/?author=1

# Combine multiple filters
GET /api/books/?author_name=John&published_year=2023&min_pages=200
\`\`\`

#### Searching
\`\`\`
# Search across title, ISBN, and author name
GET /api/books/?search=Django

# Search for specific ISBN
GET /api/books/?search=978-1234567890
\`\`\`

#### Ordering
\`\`\`
# Order by title (ascending)
GET /api/books/?ordering=title

# Order by published date (descending - newest first)
GET /api/books/?ordering=-published_date

# Order by number of pages
GET /api/books/?ordering=number_of_pages

# Multiple ordering fields
GET /api/books/?ordering=-published_date,title
\`\`\`

#### Combined Example
\`\`\`
# Get all Django books published after 2020, with more than 200 pages, ordered by date
GET /api/books/?title=Django&published_after=2020-01-01&min_pages=200&ordering=-published_date
\`\`\`

## Pagination

All list endpoints are paginated with 10 items per page by default.

\`\`\`
GET /api/books/?page=1
GET /api/books/?page=2
\`\`\`

## Example Requests

### Create an Author
\`\`\`bash
curl -X POST http://localhost:8000/api/authors/ \\
  -H "Content-Type: application/json" \\
  -u username:password \\
  -d '{
    "name": "John Doe",
    "bio": "A prolific author of technical books."
  }'
\`\`\`

### Create a Book
\`\`\`bash
curl -X POST http://localhost:8000/api/books/ \\
  -H "Content-Type: application/json" \\
  -u username:password \\
  -d '{
    "title": "Django for Beginners",
    "isbn": "978-1234567890",
    "published_date": "2023-01-15",
    "number_of_pages": 350,
    "author": 1
  }'
\`\`\`

### Get Books with Filtering
\`\`\`bash
# Get all books by a specific author published after 2020
curl "http://localhost:8000/api/books/?author_name=John&published_after=2020-01-01"

# Search for books with "Django" in title or author name
curl "http://localhost:8000/api/books/?search=Django"

# Get books ordered by publication date (newest first)
curl "http://localhost:8000/api/books/?ordering=-published_date"
\`\`\`

### Update a Book
\`\`\`bash
curl -X PUT http://localhost:8000/api/books/1/ \\
  -H "Content-Type: application/json" \\
  -u username:password \\
  -d '{
    "title": "Django for Beginners - Updated",
    "isbn": "978-1234567890",
    "published_date": "2023-01-15",
    "number_of_pages": 400,
    "author": 1
  }'
\`\`\`

### Delete a Book
\`\`\`bash
curl -X DELETE http://localhost:8000/api/books/1/ \\
  -u username:password
\`\`\`

## Response Format

### Author Response
\`\`\`json
{
  "id": 1,
  "name": "John Doe",
  "bio": "A prolific author of technical books.",
  "books": [
    {
      "id": 1,
      "title": "Django for Beginners",
      "isbn": "978-1234567890",
      "published_date": "2023-01-15",
      "number_of_pages": 350
    }
  ],
  "book_count": 1
}
\`\`\`

### Book Response
\`\`\`json
{
  "id": 1,
  "title": "Django for Beginners",
  "isbn": "978-1234567890",
  "published_date": "2023-01-15",
  "number_of_pages": 350,
  "author": 1,
  "author_name": "John Doe",
  "author_detail": {
    "id": 1,
    "name": "John Doe",
    "bio": "A prolific author of technical books.",
    "books": [...],
    "book_count": 1
  }
}
\`\`\`

## Error Responses

### Validation Error
\`\`\`json
{
  "isbn": ["ISBN must be exactly 13 digits (excluding hyphens)."],
  "published_date": ["Published date cannot be in the future."]
}
\`\`\`

### Not Found
\`\`\`json
{
  "detail": "Not found."
}
\`\`\`

### Permission Denied
\`\`\`json
{
  "detail": "Authentication credentials were not provided."
}
\`\`\`
