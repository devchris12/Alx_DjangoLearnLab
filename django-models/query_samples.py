# relationship_app/query_samples.py

"""
Django Query Samples for Advanced Model Relationships

This script demonstrates querying models with ForeignKey, ManyToMany, 
and OneToOne relationships.

To run this script:
1. First create and run migrations:
   python manage.py makemigrations relationship_app
   python manage.py migrate

2. Run this script in Django shell:
   python manage.py shell
   >>> exec(open('relationship_app/query_samples.py').read())

Or import functions individually:
   >>> from relationship_app.query_samples import *
   >>> create_sample_data()
   >>> query_books_by_author("George Orwell")
"""

from relationship_app.models import Author, Book, Library, Librarian


def create_sample_data():
    """
    Create sample data for testing queries.
    """
    print("Creating sample data...")
    
    # Create Authors
    author1, created = Author.objects.get_or_create(name="George Orwell")
    author2, created = Author.objects.get_or_create(name="Harper Lee")
    author3, created = Author.objects.get_or_create(name="J.K. Rowling")
    
    # Create Books
    book1, created = Book.objects.get_or_create(
        title="1984", 
        author=author1
    )
    book2, created = Book.objects.get_or_create(
        title="Animal Farm", 
        author=author1
    )
    book3, created = Book.objects.get_or_create(
        title="To Kill a Mockingbird", 
        author=author2
    )
    book4, created = Book.objects.get_or_create(
        title="Harry Potter and the Philosopher's Stone", 
        author=author3
    )
    book5, created = Book.objects.get_or_create(
        title="Harry Potter and the Chamber of Secrets", 
        author=author3
    )
    
    # Create Libraries
    library1, created = Library.objects.get_or_create(name="Central City Library")
    library2, created = Library.objects.get_or_create(name="Riverside Branch Library")
    library3, created = Library.objects.get_or_create(name="University Library")
    
    # Add books to libraries (ManyToMany relationships)
    library1.books.add(book1, book2, book3, book4)
    library2.books.add(book3, book4, book5)
    library3.books.add(book1, book2)
    
    # Create Librarians (OneToOne relationships)
    librarian1, created = Librarian.objects.get_or_create(
        name="Sarah Johnson",
        defaults={'library': library1}
    )
    librarian2, created = Librarian.objects.get_or_create(
        name="Michael Chen",
        defaults={'library': library2}
    )
    librarian3, created = Librarian.objects.get_or_create(
        name="Dr. Emily Rodriguez",
        defaults={'library': library3}
    )
    
    print("Sample data created successfully!")
    print()


def query_books_by_author(author_name):
    """
    Query all books by a specific author.
    Demonstrates ForeignKey relationship querying.
    """
    print("=" * 50)
    print(f"TASK 1: Query all books by '{author_name}'")
    print("=" * 50)
    
    try:
        # Get the author
        author = Author.objects.get(name=author_name)
        
        # Method 1: Using the reverse relationship (related_name='books')
        books = author.books.all()
        
        print(f"Books by {author.name}:")
        if books.exists():
            for i, book in enumerate(books, 1):
                print(f"{i}. {book.title}")
                
                # Show which libraries have this book
                libraries = book.libraries.all()
                if libraries.exists():
                    library_names = [lib.name for lib in libraries]
                    print(f"   Available at: {', '.join(library_names)}")
                else:
                    print("   Not available in any library")
        else:
            print("No books found for this author.")
        
        print(f"\nTotal books by {author.name}: {books.count()}")
        
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        print("Available authors:")
        for author in Author.objects.all():
            print(f"- {author.name}")
    
    print()


def list_books_in_library(library_name):
    """
    List all books in a library.
    Demonstrates ManyToMany relationship querying.
    """
    print("=" * 50)
    print(f"TASK 2: List all books in '{library_name}'")
    print("=" * 50)
    
    try:
        # Get the library
        library = Library.objects.get(name=library_name)
        
        # Get all books in this library using ManyToMany relationship
        books = library.books.all().select_related('author')
        
        print(f"Books in {library.name}:")
        if books.exists():
            for i, book in enumerate(books, 1):
                print(f"{i}. '{book.title}' by {book.author.name}")
        else:
            print("No books found in this library.")
        
        print(f"\nTotal books in {library.name}: {books.count()}")
        
        # Show unique authors in this library
        authors = set(book.author.name for book in books)
        if authors:
            print(f"Authors represented: {', '.join(sorted(authors))}")
        
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        print("Available libraries:")
        for library in Library.objects.all():
            print(f"- {library.name}")
    
    print()


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    Demonstrates OneToOne relationship querying.
    """
    print("=" * 50)
    print(f"TASK 3: Retrieve librarian for '{library_name}'")
    print("=" * 50)
    
    try:
        # Get the library
        library = Library.objects.get(name=library_name)
        
        print(f"Library: {library.name}")
        
        # Access the librarian using OneToOne relationship
        try:
            librarian = library.librarian
            print(f"Librarian: {librarian.name}")
            
            # Show additional information
            book_count = library.books.count()
            print(f"Books managed: {book_count}")
            
        except Librarian.DoesNotExist:
            print("No librarian assigned to this library.")
            
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        print("Available libraries:")
        for library in Library.objects.all():
            print(f"- {library.name}")
    
    print()


def demonstrate_all_queries():
    """
    Run all query demonstrations.
    """
    print("DJANGO MODEL RELATIONSHIPS DEMONSTRATION")
    print("=" * 60)
    
    # Create sample data first
    create_sample_data()
    
    # Task 1: Query books by author (ForeignKey relationship)
    query_books_by_author("George Orwell")
    query_books_by_author("J.K. Rowling")
    
    # Task 2: List books in library (ManyToMany relationship)
    list_books_in_library("Central City Library")
    list_books_in_library("Riverside Branch Library")
    
    # Task 3: Retrieve librarian for library (OneToOne relationship)
    retrieve_librarian_for_library("Central City Library")
    retrieve_librarian_for_library("University Library")
    
    print("=" * 60)
    print("All demonstrations completed!")


def show_relationship_examples():
    """
    Show additional examples of relationship querying.
    """
    print("ADDITIONAL RELATIONSHIP EXAMPLES")
    print("=" * 40)
    
    # Example 1: Find all libraries that have books by a specific author
    print("1. Libraries with George Orwell books:")
    author = Author.objects.get(name="George Orwell")
    libraries_with_orwell = Library.objects.filter(books__author=author).distinct()
    for library in libraries_with_orwell:
        print(f"   - {library.name}")
    
    print()
    
    # Example 2: Find all authors whose books are in a specific library
    print("2. Authors with books in Central City Library:")
    library = Library.objects.get(name="Central City Library")
    authors_in_library = Author.objects.filter(books__libraries=library).distinct()
    for author in authors_in_library:
        print(f"   - {author.name}")
    
    print()
    
    # Example 3: Count books per library
    print("3. Book count per library:")
    for library in Library.objects.all():
        count = library.books.count()
        print(f"   - {library.name}: {count} books")
    
    print()


# Run the demonstration if script is executed directly
if __name__ == "__main__":
    demonstrate_all_queries()
    show_relationship_examples()

# If running in Django shell, you can call:
# demonstrate_all_queries()
