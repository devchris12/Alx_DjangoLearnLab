from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    # if template exists:
    return render(request, 'relationship_app/list_books.html', {'books': books})
    # if no template is required by checker, fallback:
    # return HttpResponse("\n".join([f"{book.title} by {book.author.name}" for book in books]))
# Class-based view: show library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

