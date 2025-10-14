from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Book, Library
from django.contrib.auth.decorators import permission_required



# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# User Registration View
def register(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Role-checking functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    """
    View accessible only to Admin users.
    """
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    """
    View accessible only to Librarian users.
    """
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    """
    View accessible only to Member users.
    """
    return render(request, 'relationship_app/member_view.html')


# Permission-protected views for Book operations
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View to add a new book. Requires 'can_add_book' permission.
    """
    # Implementation for adding a book
    return render(request, 'relationship_app/add_book.html')


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """
    View to edit a book. Requires 'can_change_book' permission.
    """
    # Implementation for editing a book
    book = Book.objects.get(pk=pk)
    return render(request, 'relationship_app/edit_book.html', {'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """
    View to delete a book. Requires 'can_delete_book' permission.
    """
    # Implementation for deleting a book
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
    from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change 'home' to your desired redirect
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
    @permission_required('relationship_app.add_book')
def add_book_view(request):
    # your logic here
    pass

@permission_required('relationship_app.change_book')
def edit_book_view(request, book_id):
    # your logic here
    pass

@permission_required('relationship_app.delete_book')
def delete_book_view(request, book_id):
    # your logic here
    pass


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.book_set.all()
        return context

