from .models import Author, Book, Library, Librarian

# Query all books by a specific author
def books_by_author(author_name):
    """
    Query all books by a specific author.
    Usage: books_by_author("Author Name")
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None


# List all books in a library
def books_in_library(library_name):
    """
    List all books in a library.
    Usage: books_in_library("Library Name")
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None


# Retrieve the librarian for a library
def librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    Usage: librarian_for_library("Library Name")
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None
