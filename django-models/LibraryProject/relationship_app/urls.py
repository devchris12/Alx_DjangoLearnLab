from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Book, Library

# relationship_app/views.py

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.forms import UserCreationForm  # <--- THIS LINE IS PRESENT
from django.contrib.auth.views import LoginView, LogoutView
from .models import Book, Library

# ... (other views) ...

# LibraryProject/relationship_app/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView

urlpatterns = [
    # Login View: Uses Django's built-in LoginView
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Logout View: Uses Django's built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Redirects to home page after logout

    # Registration View: Uses the custom RegisterView you created
    path('register/', RegisterView.as_view(), name='register'),
]
# Registration View
class RegisterView(CreateView):
    form_class = UserCreationForm # <--- And it is used correctly here
    template_name = "relationship_app/register.html"
    success_url = reverse_lazy("login")
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
