# relationship_app/views.py

from django.shortcuts import render
from .views import list_books
from .models import Library, Book # Correctly import the Library model
# Correctly import the generic views you need
from django.views.generic import ListView
from .models import Book # Make sure to import the Book model
from django.views.generic import ListView, DetailView 
from django.views.generic import DetailView

from .models import Book, Library # Also import your models

class LibraryDetailView(DetailView):
    """
    This view displays details for a specific library,
    including a list of all books it contains.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html' # Specify your template
    context_object_name = 'library' # Name to use in the template
# relationship_app/views.py


class BookListView(ListView):
    """
    This view displays a list of all books with their titles and authors.
    """
    model = Book  # This implicitly does Book.objects.all()
    template_name = 'relationship_app/list_books.html' # Tells Django which template to render
    context_object_name = 'book_list' # The variable name for the book list in the template


# relationship_app/views.py



# --- Example using DetailView ---
# (For showing details of a single library)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# --- Example using ListView ---
# (For showing a list of all books)
class BookListView(ListView):
    model = Book
    template_name = 'relationship_app/book_list.html'
    context_object_name = 'book_list'
    from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

