from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Book model.
    Displays title, author, and publication_year in the list view.
    Includes search and filtering capabilities.
    """
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author']
    ordering = ['-publication_year', 'title']
