# API Usage Guide

This guide provides detailed examples of how to use the filtering, searching, and ordering features of the Advanced API Project.

## Base URL

All endpoints are prefixed with `/api/`

## Books API

### List All Books

**Endpoint:** `GET /api/books/`

**Basic Request:**
\`\`\`bash
curl http://localhost:8000/api/books/
\`\`\`

### Filtering Books

#### Filter by Exact Title
\`\`\`bash
curl "http://localhost:8000/api/books/?title=The%20Hobbit"
\`\`\`

#### Filter by Author ID
\`\`\`bash
curl "http://localhost:8000/api/books/?author=1"
\`\`\`

#### Filter by Publication Year
\`\`\`bash
curl "http://localhost:8000/api/books/?publication_year=1954"
\`\`\`

#### Filter by Year Range
\`\`\`bash
# Books published between 2000 and 2020
curl "http://localhost:8000/api/books/?publication_year_min=2000&publication_year_max=2020"
\`\`\`

#### Filter by Partial Title Match
\`\`\`bash
# Find all books with "python" in the title
curl "http://localhost:8000/api/books/?title_contains=python"
\`\`\`

#### Filter by Author Name
\`\`\`bash
# Find all books by authors with "tolkien" in their name
curl "http://localhost:8000/api/books/?author_name=tolkien"
\`\`\`

### Searching Books

Search across both title and author name:

\`\`\`bash
# Search for "django" in titles and author names
curl "http://localhost:8000/api/books/?search=django"
\`\`\`

### Ordering Books

#### Order by Title (Ascending)
\`\`\`bash
curl "http://localhost:8000/api/books/?ordering=title"
\`\`\`

#### Order by Publication Year (Descending - Newest First)
\`\`\`bash
curl "http://localhost:8000/api/books/?ordering=-publication_year"
\`\`\`

### Combining Filters, Search, and Ordering

You can combine multiple query parameters:

\`\`\`bash
# Find books published after 2000, containing "python", ordered by year
curl "http://localhost:8000/api/books/?publication_year_min=2000&title_contains=python&ordering=-publication_year"
\`\`\`

\`\`\`bash
# Search for "fantasy", filter by author, order alphabetically
curl "http://localhost:8000/api/books/?search=fantasy&author=1&ordering=title"
\`\`\`

## Authors API

### List All Authors

**Endpoint:** `GET /api/authors/`

**Basic Request:**
\`\`\`bash
curl http://localhost:8000/api/authors/
\`\`\`

### Filtering Authors

#### Filter by Exact Name
\`\`\`bash
curl "http://localhost:8000/api/authors/?name=J.R.R.%20Tolkien"
\`\`\`

#### Filter by Partial Name Match
\`\`\`bash
# Find authors with "king" in their name
curl "http://localhost:8000/api/authors/?name_contains=king"
\`\`\`

#### Filter Authors with Books
\`\`\`bash
# Only show authors who have published books
curl "http://localhost:8000/api/authors/?has_books=true"
\`\`\`

\`\`\`bash
# Only show authors without any books
curl "http://localhost:8000/api/authors/?has_books=false"
\`\`\`

### Searching Authors

\`\`\`bash
# Search for "stephen" in author names
curl "http://localhost:8000/api/authors/?search=stephen"
\`\`\`

### Ordering Authors

\`\`\`bash
# Order alphabetically by name
curl "http://localhost:8000/api/authors/?ordering=name"
\`\`\`

\`\`\`bash
# Order by ID (descending)
curl "http://localhost:8000/api/authors/?ordering=-id"
\`\`\`

### Combining Filters

\`\`\`bash
# Find authors with "king" in name who have books, ordered alphabetically
curl "http://localhost:8000/api/authors/?name_contains=king&has_books=true&ordering=name"
\`\`\`

## Creating, Updating, and Deleting

### Create a Book (Requires Authentication)

\`\`\`bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "title": "The Fellowship of the Ring",
    "publication_year": 1954,
    "author": 1
  }'
\`\`\`

### Update a Book (Requires Authentication)

\`\`\`bash
curl -X PUT http://localhost:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "title": "The Fellowship of the Ring (Updated)",
    "publication_year": 1954,
    "author": 1
  }'
\`\`\`

### Delete a Book (Requires Authentication)

\`\`\`bash
curl -X DELETE http://localhost:8000/api/books/1/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
\`\`\`

## Pagination

All list endpoints are paginated. Use the `page` parameter:

\`\`\`bash
# Get page 2 of results
curl "http://localhost:8000/api/books/?page=2"
\`\`\`

Response includes pagination metadata:
\`\`\`json
{
  "count": 50,
  "next": "http://localhost:8000/api/books/?page=3",
  "previous": "http://localhost:8000/api/books/?page=1",
  "results": [...]
}
\`\`\`

## Error Responses

### 400 Bad Request
Invalid query parameters or validation errors.

### 401 Unauthorized
Authentication required but not provided.

### 404 Not Found
Resource does not exist.

### 500 Internal Server Error
Server-side error.
