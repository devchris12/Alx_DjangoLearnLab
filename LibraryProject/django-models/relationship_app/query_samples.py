from .models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """
    Query all books by a specific author.
    
    Args:
        author_name (str): The name of the author
    
    Returns:
        QuerySet: All books by the specified author
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return Book.objects.none()


def list_books_in_library(library_name):
    """
    List all books in a library.
    
    Args:
        library_name (str): The name of the library
    
    Returns:
        QuerySet: All books in the specified library
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return Book.objects.none()


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    
    Args:
        library_name (str): The name of the library
    
    Returns:
        Librarian: The librarian object for the specified library
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")
        return None


# Example usage (can be run in Django shell)
if __name__ == "__main__":
    # These examples assume you have data in your database
    # Run these in Django shell: python manage.py shell
    
    # Example 1: Query all books by a specific author
    query_books_by_author("J.K. Rowling")
    
    # Example 2: List all books in a library
    list_books_in_library("Central Library")
    
    # Example 3: Retrieve the librarian for a library
    retrieve_librarian_for_library("Central Library")
