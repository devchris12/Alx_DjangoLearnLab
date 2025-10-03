from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm


# Authentication Views
def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('blog:post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """User profile view with edit functionality."""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('blog:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})


# Blog Post Views
class PostListView(ListView):
    """Display all blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(DetailView):
    """Display individual blog post with comments."""
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    TASK: Modify Post Creation and Update Forms
    Create new blog post with tagging support using modified PostForm.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    TASK: Modify Post Creation and Update Forms
    Update existing blog post with tagging support using modified PostForm.
    Uses LoginRequiredMixin and UserPassesTestMixin to ensure only author can edit.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        """Ensure only the author of a post can edit it."""
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete blog post.
    Uses LoginRequiredMixin and UserPassesTestMixin to ensure only author can delete.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def test_func(self):
        """Ensure only the author of a post can delete it."""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


# TASK: CRUD Operations for Comments
class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    TASK: CRUD Operations - CREATE
    Create new comment on a blog post (CREATE operation).
    Uses LoginRequiredMixin to ensure only authenticated users can comment.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        # Get the post from URL parameter
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})


@login_required
def add_comment(request, post_id):
    """
    TASK: CRUD Operations - CREATE
    Add comment to a blog post (CREATE operation).
    URL structure: /posts/int:post_id/comments/new/
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    return redirect('blog:post_detail', pk=post.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    TASK: CRUD Operations - UPDATE
    Update existing comment (UPDATE operation).
    Uses LoginRequiredMixin and UserPassesTestMixin to ensure only author can edit.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def test_func(self):
        """Ensure only the author of a comment can edit it."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    TASK: CRUD Operations - DELETE
    Delete comment (DELETE operation).
    Uses LoginRequiredMixin and UserPassesTestMixin to ensure only author can delete.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        """Ensure only the author of a comment can delete it."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        messages.success(self.request, 'Comment deleted successfully!')
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})


def search_posts(request):
    """
    TASK: Develop Search Functionality
    Search posts by title, content, or tags.
    Implements search functionality using Django's Q objects for complex queries.
    Allows users to search across multiple fields simultaneously.
    """
    query = request.GET.get('q', '')
    posts = Post.objects.all()
    
    if query:
        # TASK: Search using Q objects to search across title, content, and tags
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/search_results.html', context)


def posts_by_tag(request, tag_slug):
    """
    TASK: Integrate Tagging Functionality
    Display posts filtered by specific tag.
    Part of the tagging functionality implementation.
    """
    posts = Post.objects.filter(tags__slug=tag_slug)
    context = {
        'posts': posts,
        'tag': tag_slug,
    }
    return render(request, 'blog/posts_by_tag.html', context)
