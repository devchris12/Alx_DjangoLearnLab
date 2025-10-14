"""
Models for the API app.

This module defines the data models for managing authors and books.
The Author model represents book authors, and the Book model represents
individual books with a many-to-one relationship to authors.
"""

from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
        name: The full name of the author (max 200 characters)
    
    The Author model has a one-to-many relationship with Book,
    meaning one author can have multiple books.
    """
    name = models.CharField(max_length=200, help_text="Author's full name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
        title: The title of the book (max 300 characters)
        publication_year: The year the book was published (integer)
        author: Foreign key relationship to the Author model
    
    Relationships:
        - Many-to-one relationship with Author (many books can belong to one author)
        - Uses CASCADE deletion, so if an author is deleted, their books are also deleted
    """
    title = models.CharField(max_length=300, help_text="Book title")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author of this book"
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        ordering = ['-publication_year', 'title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
