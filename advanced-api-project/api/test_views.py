"""
Comprehensive unit tests for the API views.

This test suite covers:
- CRUD operations for Book and Author models
- Filtering, searching, and ordering functionality
- Authentication and permission enforcement
- Data validation and error handling
- Response status codes and data integrity

Run tests with: python manage.py test api
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime

from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class BookAPITestCase(TestCase):
    """
    Test suite for Book API endpoints.
    
    Tests CRUD operations, filtering, searching, ordering,
    and permission enforcement for the Book model.
    """
    
    def setUp(self):
        """
        Set up test data and client for each test.
        
        Creates:
        - An authenticated user
        - An unauthenticated client
        - An authenticated client
        - Sample authors and books
        """
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create API clients
        self.client = APIClient()
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.R.R. Tolkien')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        self.author3 = Author.objects.create(name='Brandon Sanderson')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Fellowship of the Ring',
            publication_year=1954,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='Mistborn: The Final Empire',
            publication_year=2006,
            author=self.author3
        )
        
        # API endpoints
        self.book_list_url = reverse('api:book-list')
        self.book_detail_url = lambda pk: reverse('api:book-detail', kwargs={'pk': pk})
    
    # ==================== LIST TESTS ====================
    
    def test_get_all_books(self):
        """Test retrieving all books without authentication."""
        response = self.client.get(self.book_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertIn('results', response.data)
    
    def test_get_books_pagination(self):
        """Test that pagination works correctly."""
        # Create more books to test pagination
        for i in range(15):
            Book.objects.create(
                title=f'Test Book {i}',
                publication_year=2000 + i,
                author=self.author1
            )
        
        response = self.client.get(self.book_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 10)  # Default page size
    
    # ==================== DETAIL TESTS ====================
    
    def test_get_book_detail(self):
        """Test retrieving a specific book by ID."""
        response = self.client.get(self.book_detail_url(self.book1.pk))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')
        self.assertEqual(response.data['publication_year'], 1937)
        self.assertIn('author_detail', response.data)
    
    def test_get_nonexistent_book(self):
        """Test retrieving a book that doesn't exist."""
        response = self.client.get(self.book_detail_url(9999))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ==================== CREATE TESTS ====================
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication."""
        data = {
            'title': 'The Two Towers',
            'publication_year': 1954,
            'author': self.author1.pk
        }
        
        response = self.authenticated_client.post(
            self.book_list_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['data']['title'], 'The Two Towers')
        self.assertEqual(Book.objects.count(), 5)
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(self.book_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 4)  # No new book created
    
    def test_create_book_invalid_year(self):
        """Test validation: publication year cannot be in the future."""
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        
        response = self.authenticated_client.post(
            self.book_list_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_missing_fields(self):
        """Test validation: all required fields must be provided."""
        data = {
            'title': 'Incomplete Book'
            # Missing publication_year and author
        }
        
        response = self.authenticated_client.post(
            self.book_list_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertIn('author', response.data)
    
    # ==================== UPDATE TESTS ====================
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication."""
        data = {
            'title': 'The Hobbit (Updated)',
            'publication_year': 1937,
            'author': self.author1.pk
        }
        
        response = self.authenticated_client.put(
            self.book_detail_url(self.book1.pk),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['data']['title'], 'The Hobbit (Updated)')
        
        # Verify database was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit (Updated)')
    
    def test_partial_update_book(self):
        """Test partially updating a book (PATCH)."""
        data = {
            'title': 'The Hobbit (Partial Update)'
        }
        
        response = self.authenticated_client.patch(
            self.book_detail_url(self.book1.pk),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only title was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit (Partial Update)')
        self.assertEqual(self.book1.publication_year, 1937)  # Unchanged
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1937,
            'author': self.author1.pk
        }
        
        response = self.client.put(
            self.book_detail_url(self.book1.pk),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify book was not updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit')
    
    # ==================== DELETE TESTS ====================
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication."""
        book_id = self.book1.pk
        
        response = self.authenticated_client.delete(
            self.book_detail_url(book_id)
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(Book.objects.count(), 3)
        self.assertFalse(Book.objects.filter(pk=book_id).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        response = self.client.delete(self.book_detail_url(self.book1.pk))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 4)  # Book still exists
    
    # ==================== FILTERING TESTS ====================
    
    def test_filter_books_by_author(self):
        """Test filtering books by author ID."""
        response = self.client.get(
            self.book_list_url,
            {'author': self.author1.pk}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Tolkien has 2 books
        
        # Verify all results are by the correct author
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.pk)
    
    def test_filter_books_by_publication_year(self):
        """Test filtering books by exact publication year."""
        response = self.client.get(
            self.book_list_url,
            {'publication_year': 1954}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'The Fellowship of the Ring')
    
    def test_filter_books_by_year_range(self):
        """Test filtering books by publication year range."""
        response = self.client.get(
            self.book_list_url,
            {'publication_year_min': 1950, 'publication_year_max': 2000}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # 1954 and 1996
    
    def test_filter_books_by_title_contains(self):
        """Test filtering books by partial title match."""
        response = self.client.get(
            self.book_list_url,
            {'title_contains': 'the'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should match "The Hobbit", "The Fellowship of the Ring", "A Game of Thrones"
        self.assertGreaterEqual(response.data['count'], 3)
    
    def test_filter_books_by_author_name(self):
        """Test filtering books by author name."""
        response = self.client.get(
            self.book_list_url,
            {'author_name': 'tolkien'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    # ==================== SEARCHING TESTS ====================
    
    def test_search_books(self):
        """Test searching books by title and author name."""
        response = self.client.get(
            self.book_list_url,
            {'search': 'hobbit'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'The Hobbit')
    
    def test_search_books_by_author(self):
        """Test searching books by author name."""
        response = self.client.get(
            self.book_list_url,
            {'search': 'martin'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'A Game of Thrones')
    
    def test_search_no_results(self):
        """Test searching with no matching results."""
        response = self.client.get(
            self.book_list_url,
            {'search': 'nonexistent'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
    
    # ==================== ORDERING TESTS ====================
    
    def test_order_books_by_title_ascending(self):
        """Test ordering books by title (A-Z)."""
        response = self.client.get(
            self.book_list_url,
            {'ordering': 'title'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_year_descending(self):
        """Test ordering books by publication year (newest first)."""
        response = self.client.get(
            self.book_list_url,
            {'ordering': '-publication_year'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_order_books_by_year_ascending(self):
        """Test ordering books by publication year (oldest first)."""
        response = self.client.get(
            self.book_list_url,
            {'ordering': 'publication_year'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))
    
    # ==================== COMBINED QUERY TESTS ====================
    
    def test_combined_filter_search_order(self):
        """Test combining filtering, searching, and ordering."""
        response = self.client.get(
            self.book_list_url,
            {
                'publication_year_min': 1900,
                'search': 'the',
                'ordering': 'title'
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)
        
        # Verify ordering
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))


class AuthorAPITestCase(TestCase):
    """
    Test suite for Author API endpoints.
    
    Tests CRUD operations, filtering, searching, ordering,
    and permission enforcement for the Author model.
    """
    
    def setUp(self):
        """Set up test data and clients."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create API clients
        self.client = APIClient()
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.R.R. Tolkien')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        self.author3 = Author.objects.create(name='Author Without Books')
        
        # Create test books
        Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author1
        )
        Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        # API endpoints
        self.author_list_url = reverse('api:author-list')
        self.author_detail_url = lambda pk: reverse('api:author-detail', kwargs={'pk': pk})
    
    # ==================== LIST TESTS ====================
    
    def test_get_all_authors(self):
        """Test retrieving all authors."""
        response = self.client.get(self.author_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
    
    def test_author_includes_books(self):
        """Test that author response includes nested books."""
        response = self.client.get(self.author_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Find Tolkien in results
        tolkien = next(
            author for author in response.data['results']
            if author['name'] == 'J.R.R. Tolkien'
        )
        
        self.assertIn('books', tolkien)
        self.assertEqual(len(tolkien['books']), 1)
        self.assertIn('book_count', tolkien)
    
    # ==================== DETAIL TESTS ====================
    
    def test_get_author_detail(self):
        """Test retrieving a specific author."""
        response = self.client.get(self.author_detail_url(self.author1.pk))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.R.R. Tolkien')
        self.assertIn('books', response.data)
        self.assertIn('total_books', response.data)
    
    # ==================== CREATE TESTS ====================
    
    def test_create_author_authenticated(self):
        """Test creating an author with authentication."""
        data = {'name': 'Brandon Sanderson'}
        
        response = self.authenticated_client.post(
            self.author_list_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['data']['name'], 'Brandon Sanderson')
        self.assertEqual(Author.objects.count(), 4)
    
    def test_create_author_unauthenticated(self):
        """Test that unauthenticated users cannot create authors."""
        data = {'name': 'Unauthorized Author'}
        
        response = self.client.post(self.author_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Author.objects.count(), 3)
    
    # ==================== UPDATE TESTS ====================
    
    def test_update_author_authenticated(self):
        """Test updating an author with authentication."""
        data = {'name': 'J.R.R. Tolkien (Updated)'}
        
        response = self.authenticated_client.put(
            self.author_detail_url(self.author1.pk),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, 'J.R.R. Tolkien (Updated)')
    
    # ==================== DELETE TESTS ====================
    
    def test_delete_author_authenticated(self):
        """Test deleting an author with authentication."""
        author_id = self.author3.pk
        
        response = self.authenticated_client.delete(
            self.author_detail_url(author_id)
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(Author.objects.count(), 2)
    
    def test_delete_author_cascades_books(self):
        """Test that deleting an author also deletes their books."""
        initial_book_count = Book.objects.count()
        author_book_count = self.author1.books.count()
        
        response = self.authenticated_client.delete(
            self.author_detail_url(self.author1.pk)
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Book.objects.count(),
            initial_book_count - author_book_count
        )
    
    # ==================== FILTERING TESTS ====================
    
    def test_filter_authors_with_books(self):
        """Test filtering authors who have books."""
        response = self.client.get(
            self.author_list_url,
            {'has_books': 'true'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_filter_authors_without_books(self):
        """Test filtering authors who don't have books."""
        response = self.client.get(
            self.author_list_url,
            {'has_books': 'false'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Author Without Books'
        )
    
    def test_filter_authors_by_name_contains(self):
        """Test filtering authors by partial name match."""
        response = self.client.get(
            self.author_list_url,
            {'name_contains': 'martin'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'George R.R. Martin'
        )
    
    # ==================== SEARCHING TESTS ====================
    
    def test_search_authors(self):
        """Test searching authors by name."""
        response = self.client.get(
            self.author_list_url,
            {'search': 'tolkien'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'J.R.R. Tolkien')
    
    # ==================== ORDERING TESTS ====================
    
    def test_order_authors_by_name(self):
        """Test ordering authors alphabetically."""
        response = self.client.get(
            self.author_list_url,
            {'ordering': 'name'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [author['name'] for author in response.data['results']]
        self.assertEqual(names, sorted(names))


class SerializerValidationTestCase(TestCase):
    """
    Test suite for serializer validation logic.
    
    Tests custom validation rules and data integrity checks.
    """
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name='Test Author')
    
    def test_book_serializer_future_year_validation(self):
        """Test that future publication years are rejected."""
        future_year = datetime.now().year + 1
        serializer = BookSerializer(data={
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.pk
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)
    
    def test_book_serializer_valid_data(self):
        """Test that valid book data passes validation."""
        serializer = BookSerializer(data={
            'title': 'Valid Book',
            'publication_year': 2020,
            'author': self.author.pk
        })
        
        self.assertTrue(serializer.is_valid())
        from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Author, Book

class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", publication_year=2000, author=self.author)

    def test_authenticated_create_book(self):
        # ✅ Log in the user
        self.client.login(username='testuser', password='testpass')

        response = self.client.post('/api/books/create/', {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        })

        self.assertEqual(response.status_code, 201)

    
    def test_book_serializer_unrealistic_year(self):
        """Test that unrealistically old years are rejected."""
        serializer = BookSerializer(data={
            'title': 'Ancient Book',
            'publication_year': 1000,
            'author': self.author.pk
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)
