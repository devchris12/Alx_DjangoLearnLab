# CRUD Operations Documentation

This document provides a comprehensive guide to performing Create, Read, Update, and Delete operations on the Book model using Django's ORM.

## Overview

The Book model has the following fields:
- `title`: CharField (max_length=200)
- `author`: CharField (max_length=100)
- `publication_year`: IntegerField

## Accessing the Django Shell

To perform these operations, open the Django shell:
\`\`\`bash
python manage.py shell
\`\`\`

## CREATE Operation

**File**: `create.md`

**Command**:
\`\`\`python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
\`\`\`

**Output**:
\`\`\`
# Book instance created successfully
# book.id = 1
# book.title = "1984"
# book.author = "George Orwell"
# book.publication_year = 1949
\`\`\`

## RETRIEVE Operation

**File**: `retrieve.md`

**Command**:
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(id=1)
print(book)
\`\`\`

**Output**:
\`\`\`
# 1984 by George Orwell (1949)
# book.title = "1984"
# book.author = "George Orwell"
# book.publication_year = 1949
\`\`\`

## UPDATE Operation

**File**: `update.md`

**Command**:
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
print(book)
\`\`\`

**Output**:
\`\`\`
# Nineteen Eighty-Four by George Orwell (1949)
# book.title = "Nineteen Eighty-Four"
# book.author = "George Orwell"
# book.publication_year = 1949
\`\`\`

## DELETE Operation

**File**: `delete.md`

**Command**:
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(id=1)
book.delete()
all_books = Book.objects.all()
print(all_books)
\`\`\`

**Output**:
\`\`\`
# Book deleted successfully
# Remaining books: <QuerySet []>
# (Empty queryset, confirming deletion)
\`\`\`

## Additional Useful Queries

### Retrieve All Books
\`\`\`python
from bookshelf.models import Book
all_books = Book.objects.all()
for book in all_books:
    print(book)
\`\`\`

### Filter Books by Author
\`\`\`python
books_by_orwell = Book.objects.filter(author="George Orwell")
\`\`\`

### Filter Books by Publication Year
\`\`\`python
books_1949 = Book.objects.filter(publication_year=1949)
\`\`\`

### Count Total Books
\`\`\`python
total_books = Book.objects.count()
\`\`\`

### Order Books
\`\`\`python
books_ordered = Book.objects.all().order_by('-publication_year')
