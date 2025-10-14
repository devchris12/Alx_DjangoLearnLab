"""
Custom serializers for the API app.

This module defines serializers for the Author and Book models, including:
- Nested serialization of related objects
- Custom validation logic
- Handling of complex data structures

The serializers handle the transformation between Django model instances
and JSON representations for API requests and responses.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles all fields of the Book model and includes
    custom validation to ensure data integrity.
    
    Custom Validation:
        - publication_year: Ensures the year is not in the future
    
    Fields:
        id: Auto-generated primary key (read-only)
        title: Book title
        publication_year: Year of publication (validated)
        author: Foreign key to Author (ID)
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        This prevents users from entering invalid dates.
        
        Args:
            value: The publication year to validate
            
        Returns:
            The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        # Optional: Add a reasonable lower bound (e.g., no books before printing press)
        if value < 1450:
            raise serializers.ValidationError(
                "Publication year seems unrealistic. Please enter a valid year."
            )
        
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer demonstrates advanced DRF concepts:
    - Nested serialization: Books are serialized within the author object
    - Related field handling: Uses the 'books' related_name from the model
    - Read-only nested data: Books are included in GET requests but not required for POST
    
    Relationship Handling:
        The 'books' field uses the related_name='books' defined in the Book model's
        ForeignKey relationship. This allows us to access all books by an author
        through the reverse relationship. The nested BookSerializer automatically
        serializes each related book with all its fields.
    
    Fields:
        id: Auto-generated primary key (read-only)
        name: Author's full name
        books: Nested list of all books by this author (read-only)
    """
    
    # Nested serializer for related books
    # many=True indicates this is a one-to-many relationship
    # read_only=True means books are displayed but not required when creating/updating authors
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def to_representation(self, instance):
        """
        Customize the serialized output.
        
        This method is called when serializing an Author instance to JSON.
        It allows us to modify the representation, such as adding computed fields
        or restructuring the data.
        
        Args:
            instance: The Author model instance being serialized
            
        Returns:
            Dictionary representation of the author with nested books
        """
        representation = super().to_representation(instance)
        
        # Add a computed field showing the total number of books
        representation['book_count'] = instance.books.count()
        
        return representation


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Author with additional book information.
    
    This serializer provides more detailed information about an author
    and their books, useful for detail views.
    """
    books = BookSerializer(many=True, read_only=True)
    total_books = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'total_books']
    
    def get_total_books(self, obj):
        """
        Calculate the total number of books by this author.
        
        Args:
            obj: The Author instance
            
        Returns:
            Integer count of books
        """
        return obj.books.count()


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Book with author information.
    
    This serializer includes the full author object instead of just the ID,
    providing more context in API responses.
    """
    # Nested author information (read-only)
    author_detail = AuthorSerializer(source='author', read_only=True)
    
    # Keep the author ID field for write operations
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_detail']
    
    def validate(self, data):
        """
        Object-level validation for the entire book data.
        
        This method allows validation that depends on multiple fields.
        
        Args:
            data: Dictionary of all field values
            
        Returns:
            Validated data dictionary
        """
        # Example: Ensure the book title is not empty after stripping whitespace
        if 'title' in data and not data['title'].strip():
            raise serializers.ValidationError({
                'title': 'Book title cannot be empty or just whitespace.'
            })
        
        return data
