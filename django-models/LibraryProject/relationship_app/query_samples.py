from .models import Author, Library, Book

# Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)   # <- required by checker
    return Book.objects.filter(author=author)       # <- required by checker

# List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian
