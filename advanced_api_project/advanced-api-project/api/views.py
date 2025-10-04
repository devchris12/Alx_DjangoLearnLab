from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Author, Book
from .serializers import (
    AuthorSerializer, 
    AuthorCreateSerializer,
    BookSerializer, 
    BookDetailSerializer,
    BookCreateSerializer
)
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from .filters import AuthorFilter, BookFilter


# ============================================================================
# TASK 1: Function-Based Views (FBV)
# ============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def author_list(request):
    """
    List all authors or create a new author.
    GET: Returns list of all authors
    POST: Creates a new author (requires authentication)
    """
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AuthorCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def author_detail(request, pk):
    """
    Retrieve, update or delete an author.
    GET: Returns author details
    PUT: Updates author (requires authentication)
    DELETE: Deletes author (requires authentication)
    """
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AuthorCreateSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# TASK 1: Class-Based Views (CBV)
# ============================================================================

class BookListView(APIView):
    """
    List all books or create a new book.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        """
        GET: Returns list of all books
        """
        books = Book.objects.all()
        serializer = BookDetailSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        POST: Creates a new book (requires authentication)
        """
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    """
    Retrieve, update or delete a book.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        """
        Helper method to get book object or return 404
        """
        return get_object_or_404(Book, pk=pk)
    
    def get(self, request, pk):
        """
        GET: Returns book details
        """
        book = self.get_object(pk)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        PUT: Updates book (requires authentication)
        """
        book = self.get_object(pk)
        serializer = BookCreateSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        DELETE: Deletes book (requires authentication)
        """
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# TASK 1 & 2: Generic Views with Filtering
# ============================================================================

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    Generic view for listing and creating authors.
    Includes filtering, searching, and ordering capabilities.
    """
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'id']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AuthorCreateSerializer
        return AuthorSerializer


class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieving, updating, and deleting authors.
    """
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AuthorCreateSerializer
        return AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    Generic view for listing and creating books.
    Includes filtering, searching, and ordering capabilities.
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'isbn', 'author__name']
    ordering_fields = ['title', 'published_date', 'number_of_pages', 'id']
    ordering = ['-published_date']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCreateSerializer
        return BookDetailSerializer


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieving, updating, and deleting books.
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookCreateSerializer
        return BookDetailSerializer


# ============================================================================
# TASK 2: ViewSets (Optional - for completeness)
# ============================================================================

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Author model with full CRUD operations.
    """
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'id']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AuthorCreateSerializer
        return AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model with full CRUD operations.
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'isbn', 'author__name']
    ordering_fields = ['title', 'published_date', 'number_of_pages', 'id']
    ordering = ['-published_date']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateSerializer
        return BookDetailSerializer
