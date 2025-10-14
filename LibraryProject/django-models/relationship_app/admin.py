from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['author', 'publication_year']
    search_fields = ['title', 'author__name']


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['books']


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['name', 'library']
    search_fields = ['name', 'library__name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']
