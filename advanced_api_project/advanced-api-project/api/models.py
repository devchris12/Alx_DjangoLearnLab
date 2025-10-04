from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Author(models.Model):
    """
    Author model representing book authors.
    """
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model with a many-to-one relationship to Author.
    """
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    number_of_pages = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title

    def clean(self):
        """
        Custom validation to ensure published_date is not in the future.
        """
        from django.core.exceptions import ValidationError
        if self.published_date and self.published_date > date.today():
            raise ValidationError({
                'published_date': 'Published date cannot be in the future.'
            })

    class Meta:
        ordering = ['-published_date']
