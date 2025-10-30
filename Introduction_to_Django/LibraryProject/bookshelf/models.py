from django.db import models


class Book(models.Model):
    """
    Book model representing a book in the library.
    
    Attributes:
        title: CharField with maximum length of 200 characters
        author: CharField with maximum length of 100 characters
        publication_year: IntegerField for the year of publication
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

    class Meta:
        ordering = ['-publication_year', 'title']
