# relationship_app/views.py

from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library, Book # Correctly import the Library model

class LibraryDetailView(DetailView):
    """
    This view displays details for a specific library,
    including a list of all books it contains.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html' # Specify your template
    context_object_name = 'library' # Name to use in the template
