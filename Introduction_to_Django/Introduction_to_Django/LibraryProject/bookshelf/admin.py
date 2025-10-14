from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Book model.
    
    This configuration enhances the admin interface with:
    - Custom list display showing title, author, and publication year
    - Search functionality for title and author fields
    - Filter options for publication year
    """
    # Display these fields in the admin list view
    list_display = ('title', 'author', 'publication_year')
    
    # Enable search functionality for these fields
    search_fields = ('title', 'author')
    
    # Add filters in the right sidebar
    list_filter = ('publication_year',)
    
    # Fields to display when editing a book
    fields = ('title', 'author', 'publication_year')


# Register the Book model with the custom admin configuration
admin.site.register(Book, BookAdmin)
