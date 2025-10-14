from django.test import TestCase
from .models import Book


class BookModelTest(TestCase):
    """
    Test cases for the Book model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_year=2023
        )
    
    def test_book_creation(self):
        """
        Test that a book can be created successfully.
        """
        book = Book.objects.get(title="Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.publication_year, 2023)
    
    def test_book_str_method(self):
        """
        Test the string representation of a book.
        """
        book = Book.objects.get(title="Test Book")
        self.assertEqual(str(book), "Test Book")
