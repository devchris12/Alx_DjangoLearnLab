"""
API views using Django REST Framework ViewSets.
ViewSets provide all CRUD operations automatically with filtering capabilities.
"""
from rest_framework import viewsets, filters, generics
from django_filters import rest_framework as django_filters
from .models import Book, Author
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from .serializers import BookSerializer, AuthorSerializer


class BookFilter(django_filters.FilterSet):
    """
    Filter class for Book model.
    Allows filtering by title, author, and publication_year.
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    
    Automatically provides:
    - list: GET /api/books/
    - create: POST /api/books/
    - retrieve: GET /api/books/{id}/
    - update: PUT /api/books/{id}/
    - partial_update: PATCH /api/books/{id}/
    - destroy: DELETE /api/books/{id}/
    
    Filtering:
    - Filter by title: /api/books/?title=django
    - Filter by author: /api/books/?author=john
    - Filter by year: /api/books/?publication_year=2020
    - Combine filters: /api/books/?title=django&publication_year=2020
    
    Ordering:
    - Order by title: /api/books/?ordering=title
    - Order descending: /api/books/?ordering=-title
    - Order by multiple fields: /api/books/?ordering=publication_year,-title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing author instances.
    
    Automatically provides:
    - list: GET /api/authors/
    - create: POST /api/authors/
    - retrieve: GET /api/authors/{id}/
    - update: PUT /api/authors/{id}/
    - partial_update: PATCH /api/authors/{id}/
    - destroy: DELETE /api/authors/{id}/
    """
    queryset = Author.objects.all()
serializer_class = AuthorSerializer
"""
API views using Django REST Framework ViewSets.
ViewSets provide all CRUD operations automatically with filtering capabilities.
"""
from rest_framework import viewsets, filters, generics
from django_filters import rest_framework
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookFilter(rest_framework.FilterSet):
    """
    Filter class for Book model.
    Allows filtering by title, author, and publication_year.
    """
    title = rest_framework.CharFilter(lookup_expr='icontains')
    author = rest_framework.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_year = rest_framework.NumberFilter()
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    
    Automatically provides:
    - list: GET /api/books/
    - create: POST /api/books/
    - retrieve: GET /api/books/{id}/
    - update: PUT /api/books/{id}/
    - partial_update: PATCH /api/books/{id}/
    - destroy: DELETE /api/books/{id}/
    
    Filtering:
    - Filter by title: /api/books/?title=django
    - Filter by author: /api/books/?author=john
    - Filter by year: /api/books/?publication_year=2020
    - Combine filters: /api/books/?title=django&publication_year=2020
    
    Ordering:
    - Order by title: /api/books/?ordering=title
    - Order descending: /api/books/?ordering=-title
    - Order by multiple fields: /api/books/?ordering=publication_year,-title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing author instances.
    
    Automatically provides:
    - list: GET /api/authors/
    - create: POST /api/authors/
    - retrieve: GET /api/authors/{id}/
    - update: PUT /api/authors/{id}/
    - partial_update: PATCH /api/authors/{id}/
    - destroy: DELETE /api/authors/{id}/
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Integrate filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# Retrieve a single book
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Create a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


    # Filtering by fields
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Searching by text fields
    search_fields = ['title', 'author__name']

    # Ordering by fields
    ordering_fields = ['title', 'publication_year']

