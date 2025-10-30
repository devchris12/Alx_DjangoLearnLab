# CREATE Operation

## Objective
Create a new Book instance in the database with the following details:
- Title: "1984"
- Author: "George Orwell"
- Publication Year: 1949

## Python Command

\`\`\`python
from bookshelf.models import Book

# Create a new Book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Display the created book
print(f"Book created: {book}")
print(f"Book ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
\`\`\`

## Expected Output

\`\`\`
# Book created: 1984 by George Orwell (1949)
# Book ID: 1
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
\`\`\`

## Explanation

The `Book.objects.create()` method:
1. Creates a new Book instance with the specified attributes
2. Automatically saves the instance to the database
3. Returns the created instance with an assigned primary key (id)
4. The book is now permanently stored in the database

## Verification

To verify the book was created, you can query it:
\`\`\`python
created_book = Book.objects.get(id=1)
print(created_book)
# Output: 1984 by George Orwell (1949)
