from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', include('relationship_app.urls')),
]

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
