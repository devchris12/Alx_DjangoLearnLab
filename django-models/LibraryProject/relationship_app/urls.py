from django.urls import path
from django.urls import path
from .views import list_books, LibraryDetailView, BookListView
from . import views
from django.urls import path
from . import views
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # ✅ required import
from django.contrib.auth.decorators import login_required

from django.urls import path, include
from django.contrib import admin
from django.urls import path, include

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

# Function-based view for user registration
def register_view(request):
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
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")),  # include authentication URLs
]


urlpatterns = [
    path('', include('relationship_app.urls')),
]

urlpatterns = [
    path('books/', list_books, name='list_books'),  # function-based view
    path('books/list/', BookListView.as_view(), name='book_list'),  # class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # class-based view
]


urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")  # or some dashboard
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)   # ✅ uses built-in UserCreationForm
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})
