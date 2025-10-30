from django.shortcuts import render
from .models import Book


def book_list(request):
    """View to display all books."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
