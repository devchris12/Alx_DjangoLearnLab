from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from .models import Book
from .forms import ExampleForm, SearchForm   # ← required import

@csrf_protect
def book_list(request):
    form = SearchForm(request.GET or None)
    qs = Book.objects.all()
    if form.is_valid():
        q = form.cleaned_data.get('q') or ''
        if q:
            qs = qs.filter(title__icontains=q)
    return render(request, 'bookshelf/book_list.html', {'books': qs, 'form': form})

@csrf_protect
def form_example(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)      # ← use ExampleForm
        if form.is_valid():
            Book.objects.create(title=form.cleaned_data['title'])
            messages.success(request, 'Book created securely.')
            return redirect('book_list')
    else:
        form = ExampleForm()                  # ← use ExampleForm
    return render(request, 'bookshelf/form_example.html', {'form': form})
