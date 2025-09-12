from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # required import
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView


# --- Role check helpers ---
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


# --- Role-based views ---
@user_passes_test(is_admin, raise_exception=True)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(is_librarian, raise_exception=True)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_member, raise_exception=True)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


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


# --- Authentication views ---
def register_view(request):
    """Function-based user registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after register
            messages.success(request, f"Account created for {user.username}!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


class RegisterView(CreateView):
    """Class-based user registration (alternative)"""
    form_class = UserCreationForm
    template_name = "relationship_app/register.html"
    success_url = reverse_lazy("login")


def login_view(request):
    """Function-based user login"""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


class CustomLoginView(LoginView):
    """Class-based login (alternative)"""
    template_name = "relationship_app/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")


def logout_view(request):
    """Function-based logout"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("login")


class CustomLogoutView(LogoutView):
    """Class-based logout (alternative)"""
    next_page = reverse_lazy("login")


# --- Example protected/profile views ---
@login_required
def profile_view(request):
    return render(request, "relationship_app/profile.html", {"user": request.user})

def home_view(request):
    return render(request, "relationship_app/home.html")
