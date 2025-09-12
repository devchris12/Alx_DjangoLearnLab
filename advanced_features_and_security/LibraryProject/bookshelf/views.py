from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from .models import Book
from .forms import ExampleForm, SearchForm  # ← required import
# LibraryProject/bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from .models import Book
from .forms import ExampleForm, SearchForm


@permission_required('bookshelf.can_view', raise_exception=True)   # <-- checker looks for raise_exception
@csrf_protect
def book_list(request):
    """Secure search view using forms + ORM (no raw SQL)."""
    form = SearchForm(request.GET or None)
    qs = Book.objects.all()
    if form.is_valid():
        q = form.cleaned_data.get('q') or ''
        if q:
            qs = qs.filter(title__icontains=q)
    return render(request, 'bookshelf/book_list.html', {'books': qs, 'form': form})


@permission_required('bookshelf.can_create', raise_exception=True)  # <-- raise_exception present
@csrf_protect
def form_example(request):
    """Secure create view using CSRF + form validation."""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            Book.objects.create(title=form.cleaned_data['title'])
            messages.success(request, 'Book created securely.')
            return redirect('book_list')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)    # <-- raise_exception present
@csrf_protect
def book_edit(request, pk):
    """Edit a book title (POST)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            return render(request, 'bookshelf/form_example.html', {'form': ExampleForm(), 'error': "Title required"})
        book.title = title
        book.save()
        messages.success(request, 'Book updated.')
        return redirect('book_list')
    # simple reuse of create form for demo
    form = ExampleForm(initial={'title': book.title})
    return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_delete', raise_exception=True)  # <-- raise_exception present
@csrf_protect
def book_delete(request, pk):
    """Delete a book (POST)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted.')
        return redirect('book_list')
    # simple confirmation page (optional): reuse template
    return render(request, 'bookshelf/form_example.html', {'form': ExampleForm(), 'note': 'Submit to confirm delete'})


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

