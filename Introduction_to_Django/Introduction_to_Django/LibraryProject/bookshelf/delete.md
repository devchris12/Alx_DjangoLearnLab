# Delete Operation - Django ORM

## Objective
Delete a Book instance from the database using Django's ORM.

## Command
\`\`\`python
from bookshelf.models import Book

# Retrieve the book to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# Store the title for confirmation message
book_title = book.title

# Delete the book
book.delete()

print(f"Deleted: {book_title}")

# Verify deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Total books remaining: {all_books.count()}")

# Try to retrieve the deleted book
try:
    Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Confirmed: Book no longer exists in database")
\`\`\`

## Expected Output
\`\`\`
Deleted: Nineteen Eighty-Four
Total books remaining: 0
Confirmed: Book no longer exists in database
\`\`\`

## Alternative Delete Methods

### Delete by Filter
\`\`\`python
# Delete without retrieving the object first
Book.objects.filter(title="Nineteen Eighty-Four").delete()

# Output: (1, {'bookshelf.Book': 1})
# Returns tuple: (number of objects deleted, dictionary with details)
\`\`\`

### Delete Multiple Objects
\`\`\`python
# Delete all books by a specific author
deleted_count = Book.objects.filter(author="George Orwell").delete()
print(f"Deleted {deleted_count[0]} books")
\`\`\`

### Delete All Objects
\`\`\`python
# Delete all books (use with caution!)
Book.objects.all().delete()

# Verify
print(f"Total books: {Book.objects.count()}")
# Output: Total books: 0
\`\`\`

## Important Notes
- `delete()` permanently removes the object from the database
- The method returns a tuple with the count of deleted objects
- Deleting an object also deletes related objects if CASCADE is set on foreign keys
- There is no "undo" for delete operations - always be careful!
- Consider using soft deletes (marking as inactive) for important data

## Safe Delete Pattern
\`\`\`python
# Always verify before deleting
book = Book.objects.get(title="Nineteen Eighty-Four")

# Confirm the book details before deletion
print(f"About to delete: {book.title} by {book.author}")
confirm = input("Are you sure? (yes/no): ")

if confirm.lower() == 'yes':
    book.delete()
    print("Book deleted successfully")
else:
    print("Deletion cancelled")
\`\`\`

## Checking Existence After Deletion
\`\`\`python
# Check if a book exists
exists = Book.objects.filter(title="Nineteen Eighty-Four").exists()
print(f"Book exists: {exists}")

# Output: Book exists: False
