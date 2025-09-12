from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Book, Library


# --- Function-based view ---
def list_books(request):
    """
    Function-based view to list all books with their titles and authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# --- Class-based view ---
class LibraryDetailView(DetailView):
    """
    Class-based view to display details of a specific library,
    including all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# --- Class-based view ---
class BookListView(ListView):
    """
    Class-based view to display a list of all books with their titles and authors.
    """
    model = Book
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'books'
