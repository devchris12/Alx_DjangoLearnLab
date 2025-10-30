# DELETE Operation

## Objective
Delete the Book instance and confirm the deletion by attempting to retrieve all books.

## Python Command

\`\`\`python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(id=1)

# Display book before deletion
print(f"Book before deletion: {book}")

# Delete the book
book.delete()

# Confirm deletion by retrieving all books
all_books = Book.objects.all()
print(f"All books after deletion: {all_books}")
print(f"Total books remaining: {all_books.count()}")
\`\`\`

## Expected Output

\`\`\`
# Book before deletion: 1984 by George Orwell (1949)
# All books after deletion: <QuerySet []>
# Total books remaining: 0
\`\`\`

## Explanation

The `book.delete()` method:
1. Removes the Book instance from the database
2. Returns a tuple with deletion count and details
3. The book is permanently deleted and cannot be retrieved
4. Subsequent queries will not return the deleted book

## Delete Output Details

\`\`\`python
deletion_result = book.delete()
print(deletion_result)
# Output: (1, {'bookshelf.Book': 1})
# Meaning: 1 object deleted, specifically 1 Book instance
\`\`\`

## Alternative Delete Methods

### Delete by ID
\`\`\`python
Book.objects.filter(id=1).delete()
\`\`\`

### Delete Multiple Books
\`\`\`python
Book.objects.filter(author="George Orwell").delete()
\`\`\`

### Delete All Books
\`\`\`python
Book.objects.all().delete()
\`\`\`

## Important Notes

- **Permanent**: Deletion is permanent and cannot be undone
- **Cascade**: If the Book model had foreign keys, related objects might be deleted based on cascade settings
- **Transactions**: Consider using transactions for safe bulk deletions

## Verification

To verify deletion:
\`\`\`python
try:
    book = Book.objects.get(id=1)
except Book.DoesNotExist:
    print("Book has been successfully deleted")
