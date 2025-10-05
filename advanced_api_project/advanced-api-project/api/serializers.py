from rest_framework import serializers
from .models import Author, Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer serializes all fields of the Book model.
    
    This serializer handles the Book model data and includes custom validation
    to ensure the publication_year is not in the future.
    
    Fields:
        - id: Auto-generated primary key
        - title: The book's title
        - publication_year: The year the book was published
        - author: Foreign key reference to the Author model
    
    Custom Validation:
        - validate_publication_year: Ensures the publication year is not in the future
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom validation to ensure the publication_year is not in the future.
        
        Args:
            value: The publication_year value to validate
            
        Returns:
            The validated publication_year value
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer includes the author's name and a nested BookSerializer
    to serialize the related books dynamically.
    
    This serializer demonstrates how to handle nested relationships in Django REST Framework.
    The 'books' field uses the BookSerializer to serialize all books related to an author.
    
    Fields:
        - id: Auto-generated primary key
        - name: The author's name
        - books: Nested serializer showing all books by this author (read-only)
    
    Relationship Handling:
        The relationship between Author and Book is handled through the 'books' field,
        which uses the related_name='books' defined in the Book model's ForeignKey.
        
        - many=True: Indicates that this is a one-to-many relationship (one author, many books)
        - read_only=True: The books field is read-only; books cannot be created/updated 
                          through the AuthorSerializer directly
        
        When an Author instance is serialized, the BookSerializer automatically serializes
        all related Book instances, creating a nested JSON structure like:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {"id": 1, "title": "Harry Potter", "publication_year": 1997, "author": 1},
                {"id": 2, "title": "Fantastic Beasts", "publication_year": 2001, "author": 1}
            ]
        }
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
