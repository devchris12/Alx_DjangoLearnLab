from django.urls import path
from django.urls import path
from .views import list_books, LibraryDetailView, BookListView
from . import views
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', include('relationship_app.urls')),
]

urlpatterns = [
    path('books/', list_books, name='list_books'),  # function-based view
    path('books/list/', BookListView.as_view(), name='book_list'),  # class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # class-based view
]


urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
