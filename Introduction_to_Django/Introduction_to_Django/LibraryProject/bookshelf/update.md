# Update Operation - Django ORM

## Objective
Update an existing Book instance in the database using Django's ORM.

## Command
\`\`\`python
from bookshelf.models import Book

# Retrieve the book to update
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"

# Save the changes to the database
book.save()

# Display the updated book
print(f"Updated Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
\`\`\`

## Expected Output
\`\`\`
Updated Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
\`\`\`

## Verification
\`\`\`python
# Verify the update
updated_book = Book.objects.get(id=book.id)
print(f"Verified Title: {updated_book.title}")

# Output: Verified Title: Nineteen Eighty-Four
\`\`\`

## Alternative Update Methods

### Update Multiple Fields
\`\`\`python
# Update multiple fields at once
book = Book.objects.get(title="Nineteen Eighty-Four")
book.title = "1984"
book.publication_year = 1950  # Hypothetical update
book.save()
\`\`\`

### Update Using update() Method
\`\`\`python
# Update without retrieving the object first
Book.objects.filter(title="Nineteen Eighty-Four").update(
    title="1984",
    publication_year=1949
)

# Note: This method doesn't call save() and is more efficient for bulk updates
\`\`\`

### Update Specific Fields Only
\`\`\`python
# Save only specific fields (more efficient)
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save(update_fields=['title'])
\`\`\`

## Important Notes
- Always call `save()` after modifying an object to persist changes to the database
- The `update()` method is more efficient for bulk updates but doesn't trigger model signals
- Use `update_fields` parameter in `save()` to update only specific fields
- Changes are not saved until `save()` is called

## Bulk Update Example
\`\`\`python
# Update all books by a specific author
Book.objects.filter(author="George Orwell").update(
    author="Eric Arthur Blair"  # George Orwell's real name
)

# This updates all matching records in a single query
