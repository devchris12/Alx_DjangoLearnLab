from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # required import
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView


# Function-based registration view
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Class-based registration (optional alternative)
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "relationship_app/register.html"
    success_url = reverse_lazy("login")


# Function-based login view
def login_view(request):
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


# Class-based login (optional alternative)
class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")


# Function-based logout
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("login")


# Class-based logout (optional alternative)
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")


# Protected page (requires login)
@login_required
def profile_view(request):
    return render(request, "relationship_app/profile.html", {"user": request.user})


# Simple home page
def home_view(request):
    return render(request, "relationship_app/home.html")
