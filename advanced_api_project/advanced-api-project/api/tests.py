from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from .models import Author, Book
from .serializers import AuthorSerializer, BookDetailSerializer


class AuthorModelTest(TestCase):
    """
    Test cases for the Author model.
    """
    
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            bio="A prolific author of technical books."
        )
    
    def test_author_creation(self):
        """Test that an author can be created successfully."""
        self.assertEqual(self.author.name, "John Doe")
        self.assertEqual(self.author.bio, "A prolific author of technical books.")
        self.assertEqual(str(self.author), "John Doe")
    
    def test_author_ordering(self):
        """Test that authors are ordered by name."""
        Author.objects.create(name="Alice Smith", bio="Another author")
        Author.objects.create(name="Bob Johnson", bio="Yet another author")
        
        authors = Author.objects.all()
        self.assertEqual(authors[0].name, "Alice Smith")
        self.assertEqual(authors[1].name, "Bob Johnson")
        self.assertEqual(authors[2].name, "John Doe")


class BookModelTest(TestCase):
    """
    Test cases for the Book model.
    """
    
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            bio="A prolific author."
        )
        self.book = Book.objects.create(
            title="Django for Beginners",
            isbn="978-1234567890",
            published_date=date(2023, 1, 15),
            number_of_pages=350,
            author=self.author
        )
    
    def test_book_creation(self):
        """Test that a book can be created successfully."""
        self.assertEqual(self.book.title, "Django for Beginners")
        self.assertEqual(self.book.isbn, "978-1234567890")
        self.assertEqual(self.book.number_of_pages, 350)
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(str(self.book), "Django for Beginners")
    
    def test_book_author_relationship(self):
        """Test the many-to-one relationship between Book and Author."""
        self.assertEqual(self.author.books.count(), 1)
        self.assertEqual(self.author.books.first(), self.book)
    
    def test_book_ordering(self):
        """Test that books are ordered by published_date (descending)."""
        book2 = Book.objects.create(
            title="Advanced Django",
            isbn="978-0987654321",
            published_date=date(2024, 1, 15),
            number_of_pages=450,
            author=self.author
        )
        
        books = Book.objects.all()
        self.assertEqual(books[0], book2)  # Newer book first
        self.assertEqual(books[1], self.book)


class AuthorSerializerTest(TestCase):
    """
    Test cases for the Author serializer.
    """
    
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            bio="A prolific author."
        )
        self.book = Book.objects.create(
            title="Django for Beginners",
            isbn="978-1234567890",
            published_date=date(2023, 1, 15),
            number_of_pages=350,
            author=self.author
        )
    
    def test_author_serializer_fields(self):
        """Test that the serializer contains the expected fields."""
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        
        self.assertEqual(set(data.keys()), {'id', 'name', 'bio', 'books', 'book_count'})
        self.assertEqual(data['name'], "John Doe")
        self.assertEqual(data['book_count'], 1)
        self.assertEqual(len(data['books']), 1)
    
    def test_author_name_validation_too_short(self):
        """Test that author name must be at least 2 characters."""
        from .serializers import AuthorCreateSerializer
        
        serializer = AuthorCreateSerializer(data={
            'name': 'A',
            'bio': 'A short bio for testing.'
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
    
    def test_author_name_validation_only_numbers(self):
        """Test that author name cannot contain only numbers."""
        from .serializers import AuthorCreateSerializer
        
        serializer = AuthorCreateSerializer(data={
            'name': '12345',
            'bio': 'A bio for testing.'
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class BookSerializerTest(TestCase):
    """
    Test cases for the Book serializer.
    """
    
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            bio="A prolific author."
        )
    
    def test_book_serializer_fields(self):
        """Test that the serializer contains the expected fields."""
        book = Book.objects.create(
            title="Django for Beginners",
            isbn="978-1234567890",
            published_date=date(2023, 1, 15),
            number_of_pages=350,
            author=self.author
        )
        
        serializer = BookDetailSerializer(book)
        data = serializer.data
        
        expected_fields = {
            'id', 'title', 'isbn', 'published_date', 
            'number_of_pages', 'author', 'author_name', 'author_detail'
        }
        self.assertEqual(set(data.keys()), expected_fields)
    
    def test_isbn_validation_invalid_format(self):
        """Test that ISBN must contain only digits and hyphens."""
        from .serializers import BookCreateSerializer
        
        serializer = BookCreateSerializer(data={
            'title': 'Test Book',
            'isbn': '978-ABC-123456',
            'published_date': '2023-01-15',
            'number_of_pages': 300,
            'author': self.author.id
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('isbn', serializer.errors)
    
    def test_isbn_validation_wrong_length(self):
        """Test that ISBN must be exactly 13 digits."""
        from .serializers import BookCreateSerializer
        
        serializer = BookCreateSerializer(data={
            'title': 'Test Book',
            'isbn': '978-12345',
            'published_date': '2023-01-15',
            'number_of_pages': 300,
            'author': self.author.id
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('isbn', serializer.errors)
    
    def test_published_date_validation_future(self):
        """Test that published date cannot be in the future."""
        from .serializers import BookCreateSerializer
        
        future_date = date.today() + timedelta(days=30)
        
        serializer = BookCreateSerializer(data={
            'title': 'Test Book',
            'isbn': '978-1234567890',
            'published_date': future_date.isoformat(),
            'number_of_pages': 300,
            'author': self.author.id
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('published_date', serializer.errors)
    
    def test_number_of_pages_validation(self):
        """Test that number of pages must be positive."""
        from .serializers import BookCreateSerializer
        
        serializer = BookCreateSerializer(data={
            'title': 'Test Book',
            'isbn': '978-1234567890',
            'published_date': '2023-01-15',
            'number_of_pages': 0,
            'author': self.author.id
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('number_of_pages', serializer.errors)


class AuthorAPITest(APITestCase):
    """
    Test cases for Author API endpoints.
    """
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author_data = {
            'name': 'John Doe',
            'bio': 'A prolific author of technical books.'
        }
        self.author = Author.objects.create(**self.author_data)
    
    def test_get_author_list(self):
        """Test retrieving a list of authors."""
        response = self.client.get('/api/authors/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_author_detail(self):
        """Test retrieving a single author."""
        response = self.client.get(f'/api/authors/{self.author.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')
    
    def test_create_author_authenticated(self):
        """Test creating an author with authentication."""
        self.client.force_authenticate(user=self.user)
        
        new_author_data = {
            'name': 'Jane Smith',
            'bio': 'An experienced technical writer.'
        }
        
        response = self.client.post('/api/authors/', new_author_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Jane Smith')
    
    def test_create_author_unauthenticated(self):
        """Test that creating an author requires authentication."""
        new_author_data = {
            'name': 'Jane Smith',
            'bio': 'An experienced technical writer.'
        }
        
        response = self.client.post('/api/authors/', new_author_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_author_authenticated(self):
        """Test updating an author with authentication."""
        self.client.force_authenticate(user=self.user)
        
        updated_data = {
            'name': 'John Doe Updated',
            'bio': 'An updated bio.'
        }
        
        response = self.client.put(f'/api/authors/{self.author.id}/', updated_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, 'John Doe Updated')
    
    def test_delete_author_authenticated(self):
        """Test deleting an author with authentication."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/authors/{self.author.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class BookAPITest(APITestCase):
    """
    Test cases for Book API endpoints.
    """
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(
            name='John Doe',
            bio='A prolific author.'
        )
        self.book = Book.objects.create(
            title='Django for Beginners',
            isbn='978-1234567890',
            published_date=date(2023, 1, 15),
            number_of_pages=350,
            author=self.author
        )
    
    def test_get_book_list(self):
        """Test retrieving a list of books."""
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_book_detail(self):
        """Test retrieving a single book."""
        response = self.client.get(f'/api/books/{self.book.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')
        self.assertEqual(response.data['author_name'], 'John Doe')
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication."""
        self.client.force_authenticate(user=self.user)
        
        new_book_data = {
            'title': 'Advanced Django',
            'isbn': '978-0987654321',
            'published_date': '2024-01-15',
            'number_of_pages': 450,
            'author': self.author.id
        }
        
        response = self.client.post('/api/books/', new_book_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], 'Advanced Django')
    
    def test_create_book_unauthenticated(self):
        """Test that creating a book requires authentication."""
        new_book_data = {
            'title': 'Advanced Django',
            'isbn': '978-0987654321',
            'published_date': '2024-01-15',
            'number_of_pages': 450,
            'author': self.author.id
        }
        
        response = self.client.post('/api/books/', new_book_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication."""
        self.client.force_authenticate(user=self.user)
        
        updated_data = {
            'title': 'Django for Beginners - Updated',
            'isbn': '978-1234567890',
            'published_date': '2023-01-15',
            'number_of_pages': 400,
            'author': self.author.id
        }
        
        response = self.client.put(f'/api/books/{self.book.id}/', updated_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Django for Beginners - Updated')
        self.assertEqual(self.book.number_of_pages, 400)
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/books/{self.book.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


class FilteringSearchOrderingTest(APITestCase):
    """
    Test cases for filtering, searching, and ordering functionality.
    """
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(
            name='John Doe',
            bio='A prolific author.'
        )
        self.author2 = Author.objects.create(
            name='Jane Smith',
            bio='An experienced writer.'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            isbn='978-1234567890',
            published_date=date(2023, 1, 15),
            number_of_pages=350,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Advanced Django',
            isbn='978-0987654321',
            published_date=date(2024, 6, 20),
            number_of_pages=450,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='Python Basics',
            isbn='978-1111111111',
            published_date=date(2022, 3, 10),
            number_of_pages=250,
            author=self.author2
        )
    
    def test_filter_books_by_author_name(self):
        """Test filtering books by author name."""
        response = self.client.get('/api/books/?author_name=John')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_books_by_published_year(self):
        """Test filtering books by publication year."""
        response = self.client.get('/api/books/?published_year=2023')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Django for Beginners')
    
    def test_filter_books_by_page_range(self):
        """Test filtering books by page count range."""
        response = self.client.get('/api/books/?min_pages=300&max_pages=400')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Django for Beginners')
    
    def test_search_books(self):
        """Test searching books by title, ISBN, or author name."""
        response = self.client.get('/api/books/?search=Django')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_search_authors(self):
        """Test searching authors by name or bio."""
        response = self.client.get('/api/authors/?search=Jane')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Jane Smith')
    
    def test_order_books_by_title(self):
        """Test ordering books by title."""
        response = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, ['Advanced Django', 'Django for Beginners', 'Python Basics'])
    
    def test_order_books_by_published_date_desc(self):
        """Test ordering books by published date (descending)."""
        response = self.client.get('/api/books/?ordering=-published_date')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dates = [book['published_date'] for book in response.data['results']]
        self.assertEqual(dates, ['2024-06-20', '2023-01-15', '2022-03-10'])
    
    def test_combined_filter_search_order(self):
        """Test combining filtering, searching, and ordering."""
        response = self.client.get(
            '/api/books/?author_name=John&min_pages=300&ordering=title'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, ['Advanced Django', 'Django for Beginners'])


class PaginationTest(APITestCase):
    """
    Test cases for pagination functionality.
    """
    
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            name='Test Author',
            bio='A test author.'
        )
        
        # Create 15 books to test pagination (page size is 10)
        for i in range(15):
            Book.objects.create(
                title=f'Book {i+1}',
                isbn=f'978-{str(i).zfill(10)}',
                published_date=date(2023, 1, 1),
                number_of_pages=300,
                author=self.author
            )
    
    def test_pagination_first_page(self):
        """Test that the first page returns 10 items."""
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
    
    def test_pagination_second_page(self):
        """Test that the second page returns remaining items."""
        response = self.client.get('/api/books/?page=2')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
