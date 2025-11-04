# Create Operation

## Command

```python
from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

## Expected Output

```
# Expected output: The book instance is created successfully
# The command returns: <Book: 1984>
# You can verify by checking: book.id (should show 1 or a number)
```

