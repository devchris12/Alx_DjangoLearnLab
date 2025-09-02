# relationship_app/query_samples.py
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian
from django.core.exceptions import ObjectDoesNotExist


def books_by_author(author_name: str):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        return list(author.books.values_list("title", flat=True))
    except ObjectDoesNotExist:
        return []


def books_in_library(library_name: str):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        return list(library.books.values_list("title", flat=True))
    except ObjectDoesNotExist:
        return []


def librarian_for_library(library_name: str):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian.name
    except (ObjectDoesNotExist, AttributeError):
        return None


if __name__ == "__main__":
    # Example test calls
    print("Books by Chinua Achebe:", books_by_author("Chinua Achebe"))
    print("Books in Ikeja Central Library:", books_in_library("Ikeja Central Library"))
    print("Librarian for Ikeja Central Library:", librarian_for_library("Ikeja Central Library"))
