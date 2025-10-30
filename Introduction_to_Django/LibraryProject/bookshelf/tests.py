from django.test import TestCase
from .models import Book


class BookModelTest(TestCase):
    """Test cases for the Book model."""
    
    def setUp(self):
        """Create a test book instance."""
        self.book = Book.objects.create(
            title="1984",
            author="George Orwell",
            publication_year=1949
        )
    
    def test_book_creation(self):
        """Test that a book can be created."""
        self.assertEqual(self.book.title, "1984")
        self.assertEqual(self.book.author, "George Orwell")
        self.assertEqual(self.book.publication_year, 1949)
    
    def test_book_str_representation(self):
        """Test the string representation of a book."""
        expected_str = "1984 by George Orwell (1949)"
        self.assertEqual(str(self.book), expected_str)
