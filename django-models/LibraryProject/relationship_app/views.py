from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Book, Library

# --- Role checking functions ---
def is_admin(user):
    """Check if user has Admin role"""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Check if user has Librarian role"""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Check if user has Member role"""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# --- Authentication Views ---

# Function-based view for user registration
def register(request):
    """Function-based user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Class-based view for user registration (alternative approach)
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

# Function-based view for user login
def login_view(request):
    """Function-based user login"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# Class-based login view (using Django's built-in LoginView)
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')

# Function-based view for user logout
def logout_view(request):
    """Function-based logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

# Class-based logout view (using Django's built-in LogoutView)
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# --- Role-based views using @user_passes_test decorator ---

@user_passes_test(is_admin)
def admin_view(request):
    """Admin-only view accessible only to users with Admin role"""
    return render(request, 'relationship_app/admin_view.html', {
        'user': request.user,
        'role': 'Admin'
    })

@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian-only view accessible only to users with Librarian role"""
    return render(request, 'relationship_app/librarian_view.html', {
        'user': request.user,
        'role': 'Librarian'
    })

@user_passes_test(is_member)
def member_view(request):
    """Member-only view accessible only to users with Member role"""
    return render(request, 'relationship_app/member_view.html', {
        'user': request.user,
        'role': 'Member'
    })

# --- Permission-based views ---
@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    return render(request, "relationship_app/add_book.html")

@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request):
    return render(request, "relationship_app/edit_book.html")

@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request):
    return render(request, "relationship_app/delete_book.html")

# --- Book and Library Views ---

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

# --- Protected and General Views ---

@login_required
def profile_view(request):
    """Protected user profile view"""
    return render(request, 'relationship_app/profile.html', {'user': request.user})

def home_view(request):
    """Home page view"""
    return render(request, 'relationship_app/home.html')
