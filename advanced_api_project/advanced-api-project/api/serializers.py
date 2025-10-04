from rest_framework import serializers
from .models import Author, Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """
    Basic Book serializer for nested representation in AuthorSerializer.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'published_date', 'number_of_pages']


class AuthorSerializer(serializers.ModelSerializer):
    """
    Author serializer with nested books representation.
    Includes custom validation for name field.
    """
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'books', 'book_count']

    def get_book_count(self, obj):
        """
        Returns the total number of books by this author.
        """
        return obj.books.count()

    def validate_name(self, value):
        """
        Custom validation: Ensure name is at least 2 characters long
        and doesn't contain only numbers.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "Author name must be at least 2 characters long."
            )
        
        if value.isdigit():
            raise serializers.ValidationError(
                "Author name cannot contain only numbers."
            )
        
        return value


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Detailed Book serializer with author information and custom validation.
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_detail = AuthorSerializer(source='author', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 
            'title', 
            'isbn', 
            'published_date', 
            'number_of_pages', 
            'author',
            'author_name',
            'author_detail'
        ]
        read_only_fields = ['id']

    def validate_isbn(self, value):
        """
        Custom validation: Ensure ISBN is exactly 13 characters
        and contains only digits and hyphens.
        """
        # Remove hyphens for validation
        isbn_digits = value.replace('-', '')
        
        if not isbn_digits.isdigit():
            raise serializers.ValidationError(
                "ISBN must contain only digits and hyphens."
            )
        
        if len(isbn_digits) != 13:
            raise serializers.ValidationError(
                "ISBN must be exactly 13 digits (excluding hyphens)."
            )
        
        return value

    def validate_published_date(self, value):
        """
        Custom validation: Ensure published date is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError(
                "Published date cannot be in the future."
            )
        
        return value

    def validate_number_of_pages(self, value):
        """
        Custom validation: Ensure number of pages is positive and reasonable.
        """
        if value < 1:
            raise serializers.ValidationError(
                "Number of pages must be at least 1."
            )
        
        if value > 10000:
            raise serializers.ValidationError(
                "Number of pages seems unreasonably high (max 10,000)."
            )
        
        return value

    def validate(self, data):
        """
        Object-level validation: Ensure books published before 1450
        have fewer than 500 pages (early printing era).
        """
        published_date = data.get('published_date')
        number_of_pages = data.get('number_of_pages')
        
        if published_date and number_of_pages:
            if published_date.year < 1450 and number_of_pages > 500:
                raise serializers.ValidationError(
                    "Books published before 1450 (pre-printing press era) "
                    "typically had fewer than 500 pages."
                )
        
        return data


class BookCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating books with simplified fields.
    """
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'published_date', 'number_of_pages', 'author']

    def validate_isbn(self, value):
        """
        Custom validation: Ensure ISBN is exactly 13 characters
        and contains only digits and hyphens.
        """
        isbn_digits = value.replace('-', '')
        
        if not isbn_digits.isdigit():
            raise serializers.ValidationError(
                "ISBN must contain only digits and hyphens."
            )
        
        if len(isbn_digits) != 13:
            raise serializers.ValidationError(
                "ISBN must be exactly 13 digits (excluding hyphens)."
            )
        
        return value

    def validate_published_date(self, value):
        """
        Custom validation: Ensure published date is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError(
                "Published date cannot be in the future."
            )
        
        return value


class AuthorCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating authors with validation.
    """
    class Meta:
        model = Author
        fields = ['name', 'bio']

    def validate_name(self, value):
        """
        Custom validation: Ensure name is at least 2 characters long
        and doesn't contain only numbers.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "Author name must be at least 2 characters long."
            )
        
        if value.isdigit():
            raise serializers.ValidationError(
                "Author name cannot contain only numbers."
            )
        
        return value

    def validate_bio(self, value):
        """
        Custom validation: Ensure bio is at least 10 characters long.
        """
        if len(value) < 10:
            raise serializers.ValidationError(
                "Author bio must be at least 10 characters long."
            )
        
        return value
