from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class CustomUserCreationForm(UserCreationForm):
    """Extended user registration form with email field."""
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile information."""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    Modified to include tags field for tagging functionality.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Tags field added for tagging functionality
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Write your post content...'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add tags separated by commas'}),
        }
        help_texts = {
            'tags': 'Separate tags with commas (e.g., python, django, web-development)',
        }
    
    def clean_title(self):
        """Validate post title."""
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError('Title cannot be empty.')
        if len(title.strip()) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title.strip()
    
    def clean_content(self):
        """Validate post content."""
        content = self.cleaned_data.get('content')
        if not content or not content.strip():
            raise forms.ValidationError('Content cannot be empty.')
        if len(content.strip()) < 10:
            raise forms.ValidationError('Content must be at least 10 characters long.')
        return content.strip()


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments with validation rules.
    Developed using Django's ModelForm to facilitate comment creation and updating.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }
        labels = {
            'content': 'Comment',
        }
    
    def clean_content(self):
        """
        Validate comment content with necessary validation rules.
        Ensures content is not empty, meets minimum length, and doesn't exceed maximum length.
        """
        content = self.cleaned_data.get('content')
        
        # Ensure content is not empty or just whitespace
        if not content or not content.strip():
            raise forms.ValidationError('Comment cannot be empty.')
        
        # Ensure minimum length
        if len(content.strip()) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        
        # Ensure maximum length
        if len(content) > 1000:
            raise forms.ValidationError('Comment cannot exceed 1000 characters.')
        
        return content.strip()
