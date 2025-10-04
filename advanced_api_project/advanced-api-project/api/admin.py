from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'published_date', 'number_of_pages']
    list_filter = ['published_date', 'author']
    search_fields = ['title', 'isbn', 'author__name']
    date_hierarchy = 'published_date'
