"""
Admin configuration for the API app.
"""

from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for Author model."""
    list_display = ['name', 'book_count']
    search_fields = ['name']
    
    def book_count(self, obj):
        """Display the number of books by this author."""
        return obj.books.count()
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface for Book model."""
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    autocomplete_fields = ['author']
