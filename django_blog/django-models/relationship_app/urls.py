from django.urls import path
from . import views

urlpatterns = [
    # Book listing views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Role-based access URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Permission-based book operation URLs
    path('books/add/', views.add_book_view, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book_view, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book_view, name='delete_book'),
]
