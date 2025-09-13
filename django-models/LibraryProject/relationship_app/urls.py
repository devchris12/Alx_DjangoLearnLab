from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Book, Library

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view: display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# Class-based view: display all books
class BookListView(ListView):
    model = Book
    template_name = "relationship_app/book_list.html"
    context_object_name = "book_list"

# Registration View
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "relationship_app/register.html"
    success_url = reverse_lazy("login")
