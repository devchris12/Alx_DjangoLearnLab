# CRUD Operations Documentation

This document contains all the CRUD (Create, Read, Update, Delete) operations performed on the Book model using Django's ORM through the Django shell.

## Setup
First, open the Django shell:
\`\`\`bash
python manage.py shell
\`\`\`

Then import the Book model:
\`\`\`python
from bookshelf.models import Book
\`\`\`

---

## CREATE Operation

### Command:
\`\`\`python
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
print(f"Created: {book.title} by {book.author} ({book.publication_year})")
print(f"Book ID: {book.id}")
\`\`\`

### Output:
\`\`\`
Created: 1984 by George Orwell (1949)
Book ID: 1
\`\`\`

---

## RETRIEVE Operation

### Command:
\`\`\`python
book = Book.objects.get(title="1984")
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
\`\`\`

### Output:
\`\`\`
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
\`\`\`

### Additional Retrieve Examples:

#### Get All Books:
\`\`\`python
all_books = Book.objects.all()
for book in all_books:
    print(f"{book.title} by {book.author}")
\`\`\`

Output:
\`\`\`
1984 by George Orwell
\`\`\`

#### Filter Books:
\`\`\`python
orwell_books = Book.objects.filter(author="George Orwell")
print(f"Found {orwell_books.count()} book(s) by George Orwell")
\`\`\`

Output:
\`\`\`
Found 1 book(s) by George Orwell
\`\`\`

---

## UPDATE Operation

### Command:
\`\`\`python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
\`\`\`

### Output:
\`\`\`
Updated Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
\`\`\`

### Verification:
\`\`\`python
updated_book = Book.objects.get(id=book.id)
print(f"Verified Title: {updated_book.title}")
\`\`\`

Output:
\`\`\`
Verified Title: Nineteen Eighty-Four
\`\`\`

---

## DELETE Operation

### Command:
\`\`\`python
book = Book.objects.get(title="Nineteen Eighty-Four")
book_title = book.title
book.delete()
print(f"Deleted: {book_title}")

# Verify deletion
all_books = Book.objects.all()
print(f"Total books remaining: {all_books.count()}")

# Confirm the book no longer exists
try:
    Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Confirmed: Book no longer exists in database")
\`\`\`

### Output:
\`\`\`
Deleted: Nineteen Eighty-Four
Total books remaining: 0
Confirmed: Book no longer exists in database
\`\`\`

---

## Summary

All CRUD operations have been successfully demonstrated:

1. ✅ **CREATE**: Created a Book instance with title "1984", author "George Orwell", and publication year 1949
2. ✅ **RETRIEVE**: Retrieved and displayed all attributes of the created book
3. ✅ **UPDATE**: Updated the book title from "1984" to "Nineteen Eighty-Four"
4. ✅ **DELETE**: Deleted the book and confirmed its removal from the database

## Additional Resources

For more detailed information on each operation, see:
- `create.md` - Detailed CREATE operation documentation
- `retrieve.md` - Detailed RETRIEVE operation documentation
- `update.md` - Detailed UPDATE operation documentation
- `delete.md` - Detailed DELETE operation documentation
