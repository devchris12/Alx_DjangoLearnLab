import django_filters
from .models import Author, Book


class AuthorFilter(django_filters.FilterSet):
    """
    Custom filter for Author model.
    Allows filtering by name (exact and partial match).
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    name_exact = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    
    class Meta:
        model = Author
        fields = ['name']


class BookFilter(django_filters.FilterSet):
    """
    Custom filter for Book model.
    Allows filtering by multiple fields with various lookup types.
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    published_year = django_filters.NumberFilter(field_name='published_date', lookup_expr='year')
    published_after = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_before = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')
    min_pages = django_filters.NumberFilter(field_name='number_of_pages', lookup_expr='gte')
    max_pages = django_filters.NumberFilter(field_name='number_of_pages', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'isbn': ['exact'],
            'author': ['exact'],
            'published_date': ['exact', 'year', 'gte', 'lte'],
            'number_of_pages': ['exact', 'gte', 'lte'],
        }
