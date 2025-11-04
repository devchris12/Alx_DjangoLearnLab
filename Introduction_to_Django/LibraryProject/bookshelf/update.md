# Update Operation

## Command

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

## Expected Output

```
# Expected output:
# Updated title: Nineteen Eighty-Four
# The book instance is successfully updated in the database
```

