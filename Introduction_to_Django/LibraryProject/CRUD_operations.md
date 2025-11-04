# CRUD Operations Documentation

This document contains all CRUD (Create, Read, Update, Delete) operations performed on the Book model using Django's ORM via the Django shell.

## Prerequisites

Before running these commands, ensure you have:
1. Created and migrated the Book model
2. Opened the Django shell using: `python manage.py shell`

## Operations

### 1. Create Operation

**Command:**
```python
from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

**Expected Output:**
```
# The book instance is created successfully
# The command returns: <Book: 1984>
# You can verify by checking: book.id (should show 1 or a number)
```

### 2. Retrieve Operation

**Command:**
```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

**Expected Output:**
```
# Expected output:
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
```

### 3. Update Operation

**Command:**
```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

**Expected Output:**
```
# Expected output:
# Updated title: Nineteen Eighty-Four
# The book instance is successfully updated in the database
```

### 4. Delete Operation

**Command:**
```python
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Number of books remaining: {all_books.count()}")
```

**Expected Output:**
```
# Expected output:
# Number of books remaining: 0
# The book has been successfully deleted from the database
```

