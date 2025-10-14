"""
Custom filters for the API app.

This module defines custom filter classes that extend django-filter
functionality to provide advanced filtering capabilities for the API.

The filters allow API consumers to:
- Filter by exact matches
- Filter by ranges (e.g., publication year between two values)
- Filter by partial matches (case-insensitive)
- Combine multiple filters
"""

from django_filters import rest_framework as filters
from .models import Book, Author


class BookFilter(filters.FilterSet):
    """
    Custom filter for the Book model.
    
    This filter provides multiple ways to query books:
    
    Exact Filters:
        - title: Exact match on book title
        - author: Filter by author ID
        - publication_year: Exact year match
    
    Range Filters:
        - publication_year_min: Books published on or after this year
        - publication_year_max: Books published on or before this year
    
    Partial Match Filters:
        - title_contains: Case-insensitive partial match on title
        - author_name: Case-insensitive partial match on author name
    
    Example Usage:
        /api/books/?title_contains=python
        /api/books/?publication_year_min=2000&publication_year_max=2020
        /api/books/?author_name=tolkien
    """
    
    # Exact match filters
    title = filters.CharFilter(field_name='title', lookup_expr='iexact')
    author = filters.NumberFilter(field_name='author__id')
    publication_year = filters.NumberFilter(field_name='publication_year')
    
    # Range filters for publication year
    publication_year_min = filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        label='Published on or after year'
    )
    publication_year_max = filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        label='Published on or before year'
    )
    
    # Partial match filters
    title_contains = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title contains (case-insensitive)'
    )
    author_name = filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        label='Author name contains (case-insensitive)'
    )
    
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'publication_year',
            'publication_year_min',
            'publication_year_max',
            'title_contains',
            'author_name',
        ]


class AuthorFilter(filters.FilterSet):
    """
    Custom filter for the Author model.
    
    Filters:
        - name: Exact match on author name (case-insensitive)
        - name_contains: Partial match on author name
        - has_books: Filter authors who have/don't have books
    
    Example Usage:
        /api/authors/?name_contains=king
        /api/authors/?has_books=true
    """
    
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    name_contains = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Name contains (case-insensitive)'
    )
    
    # Filter authors based on whether they have books
    has_books = filters.BooleanFilter(
        method='filter_has_books',
        label='Has published books'
    )
    
    def filter_has_books(self, queryset, name, value):
        """
        Custom filter method to find authors with or without books.
        
        Args:
            queryset: The initial queryset
            name: The filter field name
            value: Boolean - True for authors with books, False for authors without
        
        Returns:
            Filtered queryset
        """
        if value:
            # Authors with at least one book
            return queryset.filter(books__isnull=False).distinct()
        else:
            # Authors with no books
            return queryset.filter(books__isnull=True)
    
    class Meta:
        model = Author
        fields = ['name', 'name_contains', 'has_books']
