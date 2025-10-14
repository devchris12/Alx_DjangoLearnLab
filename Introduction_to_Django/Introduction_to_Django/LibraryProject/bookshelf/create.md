# Create Operation - Django ORM

## Objective
Create a new Book instance in the database using Django's ORM.

## Command
\`\`\`python
from bookshelf.models import Book

# Create a new Book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Display the created book
print(f"Created: {book.title} by {book.author} ({book.publication_year})")
print(f"Book ID: {book.id}")
\`\`\`

## Expected Output
\`\`\`
Created: 1984 by George Orwell (1949)
Book ID: 1
\`\`\`

## Explanation
- `Book.objects.create()` creates a new Book instance and saves it to the database in one step
- The method returns the created object, which we store in the `book` variable
- The book is automatically assigned an ID (primary key) by Django
- The object is immediately saved to the database

## Alternative Method
\`\`\`python
# Create an instance without saving
book = Book(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Save to database
book.save()
\`\`\`

## Verification
To verify the book was created:
\`\`\`python
# Check if the book exists
Book.objects.filter(title="1984").exists()
# Output: True

# Count total books
Book.objects.count()
# Output: 1
