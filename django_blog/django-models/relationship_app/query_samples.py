from .models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return None


def list_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None


def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")
        return None


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     # Query books by author
#     query_books_by_author("J.K. Rowling")
#     
#     # List books in library
#     list_books_in_library("Central Library")
#     
#     # Retrieve librarian for library
#     retrieve_librarian_for_library("Central Library")
