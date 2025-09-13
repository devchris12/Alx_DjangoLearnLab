from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
# LibraryProject/relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView, BookListView, register
from .views import add_book, edit_book, delete_book   # 👈 import the new views

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books, LibraryDetailView, BookListView


urlpatterns = [
    path("books/", list_books, name="list_books"),                     # function-based
    path("books/list/", BookListView.as_view(), name="book_list"),     # CBV for all books
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),  # CBV for a library
]


urlpatterns = [
    # Authentication URLs - Required patterns
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Protected views
    path('profile/', views.profile_view, name='profile'),
    
    # Role-based views
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Permission-based book management views
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/', views.edit_book, name='edit_book'),
    path('delete_book/', views.delete_book, name='delete_book'),
    
    # Book and Library views
    path('books/', views.list_books, name='list_books'),
    path('books/class/', views.BookListView.as_view(), name='book_list_class'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Home page
    path('', views.home_view, name='home'),
]
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

