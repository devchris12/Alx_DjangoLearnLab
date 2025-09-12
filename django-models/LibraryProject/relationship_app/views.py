from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

# Function-based view: list all books with titles and authors
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view: display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Optional: class-based list view for all books
class BookListView(ListView):
    model = Book
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'book_list'
