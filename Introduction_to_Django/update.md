# UPDATE Operation

## Objective
Update the title of the Book instance from "1984" to "Nineteen Eighty-Four" and save the changes.

## Python Command

\`\`\`python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(id=1)

# Display original title
print(f"Original title: {book.title}")

# Update the title
book.title = "Nineteen Eighty-Four"

# Save the changes to the database
book.save()

# Display updated book
print(f"Updated book: {book}")
print(f"New title: {book.title}")
\`\`\`

## Expected Output

\`\`\`
# Original title: 1984
# Updated book: Nineteen Eighty-Four by George Orwell (1949)
# New title: Nineteen Eighty-Four
\`\`\`

## Explanation

The update process involves three steps:
1. **Retrieve**: Get the Book instance using `Book.objects.get()`
2. **Modify**: Change the attribute value (e.g., `book.title = "new value"`)
3. **Save**: Call `book.save()` to persist changes to the database

## Alternative Update Methods

### Using update() for Multiple Records
\`\`\`python
Book.objects.filter(author="George Orwell").update(title="Nineteen Eighty-Four")
\`\`\`

### Update Multiple Fields
\`\`\`python
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.publication_year = 1949
book.save()
\`\`\`

### Bulk Update
\`\`\`python
books = Book.objects.all()
for book in books:
    book.title = book.title.upper()
Book.objects.bulk_update(books, ['title'])
\`\`\`

## Verification

To verify the update:
\`\`\`python
updated_book = Book.objects.get(id=1)
print(updated_book.title)
# Output: Nineteen Eighty-Four
