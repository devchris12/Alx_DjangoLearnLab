from django.db import models
from datetime import date


class Author(models.Model):
    """
    Author model representing book authors.
    
    Fields:
        name: A string field to store the author's name.
    
    Relationships:
        books: One-to-many relationship with Book model (one author can have multiple books).
    """
    name = models.CharField(max_length=100, help_text="The author's full name")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model with a many-to-one relationship to Author.
    
    Fields:
        title: A string field for the book's title.
        publication_year: An integer field for the year the book was published.
        author: A foreign key linking to the Author model, establishing a one-to-many 
                relationship from Author to Books.
    
    Relationships:
        author: Many-to-one relationship with Author model (many books can belong to one author).
                Uses CASCADE deletion - if an author is deleted, all their books are also deleted.
                The related_name='books' allows accessing all books by an author via author.books.all()
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author who wrote this book"
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

    class Meta:
        ordering = ['-publication_year']
