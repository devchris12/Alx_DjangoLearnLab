from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
# LibraryProject/relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView, BookListView, register
from .views import add_book, edit_book, delete_book   # 👈 import the new views

urlpatterns = [
    # Authentication URLs - Required patterns
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Protected views
    path('profile/', views.profile_view, name='profile'),
    
    # Home page
    path('', views.home_view, name='home'),
]
urlpatterns = [
    # Existing book & library views
    path("books/", list_books, name="list_books"),
    path("books/list/", BookListView.as_view(), name="book_list"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Authentication
    path("register/", register, name="register"),

    # 🔒 Permission-protected book management URLs
    path("books/add/", add_book, name="add_book"),
    path("books/<int:book_id>/edit/", edit_book, name="edit_book"),
    path("books/<int:book_id>/delete/", delete_book, name="delete_book"),
]

