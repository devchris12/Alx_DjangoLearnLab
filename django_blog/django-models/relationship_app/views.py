from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from .models import Book, Library


# Function-based view to list all books
def list_books(request):
    """Function-based view to list all books."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """Class-based view to display details of a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Authentication Views
def register_view(request):
    """View for user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def login_view(request):
    """View for user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


def logout_view(request):
    """View for user logout."""
    logout(request)
    return render(request, 'relationship_app/logout.html')


# Role-based access control helper functions
def is_admin(user):
    """Check if user has Admin role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    """Check if user has Librarian role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    """Check if user has Member role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only to Admin users."""
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users."""
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    """View accessible only to Member users."""
    return render(request, 'relationship_app/member_view.html')


# Permission-based views for book operations
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book_view(request):
    """View to add a new book (requires can_add_book permission)."""
    if request.method == 'POST':
        # Add book creation logic here
        messages.success(request, 'Book added successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book_view(request, pk):
    """View to edit a book (requires can_change_book permission)."""
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        # Add book editing logic here
        messages.success(request, 'Book updated successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book_view(request, pk):
    """View to delete a book (requires can_delete_book permission)."""
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
