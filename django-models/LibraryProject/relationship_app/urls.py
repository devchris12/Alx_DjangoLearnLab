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
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

# Function-based view for user registration
def register(request):
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'relationship_app/login.html')

# Class-based login view (using Django's built-in LoginView)
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')

# Function-based view for user logout
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

# Class-based logout view (using Django's built-in LogoutView)
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# Example of a protected view that requires login
@login_required
def profile_view(request):
    return render(request, 'relationship_app/profile.html', {'user': request.user})

# Home view (example)
def home_view(request):
    return render(request, 'relationship_app/home.html')
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
