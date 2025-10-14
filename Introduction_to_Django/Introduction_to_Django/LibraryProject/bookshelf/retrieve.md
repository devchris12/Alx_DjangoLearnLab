# Retrieve Operation - Django ORM

## Objective
Retrieve and display book data from the database using Django's ORM.

## Command
\`\`\`python
from bookshelf.models import Book

# Retrieve the book by title
book = Book.objects.get(title="1984")

# Display all attributes
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
\`\`\`

## Expected Output
\`\`\`
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
\`\`\`

## Additional Retrieve Methods

### Retrieve All Books
\`\`\`python
# Get all books
all_books = Book.objects.all()

for book in all_books:
    print(f"{book.title} by {book.author}")

# Output: 1984 by George Orwell
\`\`\`

### Filter Books
\`\`\`python
# Filter books by author
orwell_books = Book.objects.filter(author="George Orwell")

for book in orwell_books:
    print(book.title)

# Output: 1984
\`\`\`

### Get First Book
\`\`\`python
# Get the first book
first_book = Book.objects.first()
print(first_book.title)

# Output: 1984
\`\`\`

### Get by ID
\`\`\`python
# Retrieve by primary key
book = Book.objects.get(pk=1)
print(book.title)

# Output: 1984
\`\`\`

## Important Notes
- `get()` returns a single object and raises an exception if no match or multiple matches are found
- `filter()` returns a QuerySet (can contain zero, one, or multiple objects)
- `all()` returns all objects in the database
- Always handle potential `DoesNotExist` exceptions when using `get()`

## Error Handling
\`\`\`python
from django.core.exceptions import ObjectDoesNotExist

try:
    book = Book.objects.get(title="Nonexistent Book")
except ObjectDoesNotExist:
    print("Book not found")
