from django.apps import AppConfig


class BookshelfConfig(AppConfig):
    """
    Configuration class for the bookshelf application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookshelf'
    verbose_name = 'Book Management'
