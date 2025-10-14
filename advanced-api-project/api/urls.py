"""
URL routing for the API app.

This module defines the URL patterns for all API endpoints,
mapping URLs to their corresponding views using Django REST Framework routers.

Endpoints:
    Books:
        - GET/POST           /api/books/          List books or create new book
        - GET/PUT/PATCH/DELETE /api/books/<id>/    Retrieve, update, or delete book
    
    Authors:
        - GET/POST           /api/authors/        List authors or create new author
        - GET/PUT/PATCH/DELETE /api/authors/<id>/  Retrieve, update, or delete author

The router automatically generates these URL patterns:
    - GET    /api/books/          -> list all books
    - POST   /api/books/          -> create a new book
    - GET    /api/books/{id}/     -> retrieve a specific book
    - PUT    /api/books/{id}/     -> update a specific book (full update)
    - PATCH  /api/books/{id}/     -> partial update a specific book
    - DELETE /api/books/{id}/     -> delete a specific book
    (Same pattern applies to /api/authors/)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet

# App namespace for URL reversing
app_name = 'api'

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author')

# Include router-generated URLs
urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path
from .views import (
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    BookListView
)
from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),  # ✅ Matches "books/update"
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),  # ✅ Matches "books/delete"
    path('books/create/', BookCreateView.as_view(), name='book-create'),
]


urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]

