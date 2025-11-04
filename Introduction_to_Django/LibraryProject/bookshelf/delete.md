# Delete Operation

## Command

```python
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Number of books remaining: {all_books.count()}")
```

## Expected Output

```
# Expected output:
# Number of books remaining: 0
# The book has been successfully deleted from the database
```

