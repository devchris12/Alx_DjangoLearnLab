from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router for ViewSets
router = DefaultRouter()
router.register(r'viewset-authors', views.AuthorViewSet, basename='viewset-author')
router.register(r'viewset-books', views.BookViewSet, basename='viewset-book')

urlpatterns = [
    # Function-Based Views (FBV)
    path('fbv/authors/', views.author_list, name='fbv-author-list'),
    path('fbv/authors/<int:pk>/', views.author_detail, name='fbv-author-detail'),
    
    # Class-Based Views (CBV)
    path('cbv/books/', views.BookListView.as_view(), name='cbv-book-list'),
    path('cbv/books/<int:pk>/', views.BookDetailView.as_view(), name='cbv-book-detail'),
    
    # Generic Views (with filtering support)
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDestroyView.as_view(), name='author-detail'),
    path('books/', views.BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    
    # ViewSet routes
    path('', include(router.urls)),
]
