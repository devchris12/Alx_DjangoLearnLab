# RETRIEVE Operation

## Objective
Retrieve and display all attributes of the Book instance created in the CREATE operation.

## Python Command

\`\`\`python
from bookshelf.models import Book

# Retrieve the book by ID
book = Book.objects.get(id=1)

# Display all attributes
print(f"Book: {book}")
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

# Alternative: Retrieve all books
all_books = Book.objects.all()
for b in all_books:
    print(b)
\`\`\`

## Expected Output

\`\`\`
# Book: 1984 by George Orwell (1949)
# ID: 1
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
\`\`\`

## Explanation

The `Book.objects.get()` method:
1. Queries the database for a Book with the specified ID
2. Returns a single Book instance
3. Raises `DoesNotExist` exception if no book is found
4. Raises `MultipleObjectsReturned` if multiple books match the criteria

## Alternative Retrieval Methods

### Get All Books
\`\`\`python
all_books = Book.objects.all()
\`\`\`

### Filter Books
\`\`\`python
books_by_author = Book.objects.filter(author="George Orwell")
\`\`\`

### Get First Book
\`\`\`python
first_book = Book.objects.first()
\`\`\`

### Count Books
\`\`\`python
total_count = Book.objects.count()
