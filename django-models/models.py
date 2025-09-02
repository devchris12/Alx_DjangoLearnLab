# relationship_app/models.py

from django.db import models


class Author(models.Model):
    """
    Author model representing book authors.
    This demonstrates the 'One' side of a One-to-Many (ForeignKey) relationship with Book.
    """
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing individual books.
    This demonstrates:
    - ForeignKey relationship (Many-to-One) with Author
    - The 'Many' side of Many-to-Many relationship with Library
    """
    title = models.CharField(max_length=300)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='books'
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']


class Library(models.Model):
    """
    Library model representing library branches.
    This demonstrates:
    - ManyToManyField relationship with Book
    - The 'One' side of One-to-One relationship with Librarian
    """
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(
        Book,
        related_name='libraries',
        blank=True
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Libraries"


class Librarian(models.Model):
    """
    Librarian model representing library staff.
    This demonstrates OneToOneField relationship with Library.
    """
    name = models.CharField(max_length=200)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        related_name='librarian'
    )
    
    def __str__(self):
        return f"{self.name} - {self.library.name}"
    
    class Meta:
        ordering = ['name']
