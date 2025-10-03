# Django Blog Project

A comprehensive blog application built with Django that includes user authentication, blog post management, comments, tagging, and search functionality.

## Features

### 1. User Authentication System
- User registration with email validation
- Login and logout functionality
- User profile management
- Password security with Django's built-in hashing

### 2. Blog Post Management (CRUD)
- Create new blog posts (authenticated users only)
- View all blog posts (public access)
- View individual post details
- Edit posts (authors only)
- Delete posts (authors only)
- Automatic author assignment based on logged-in user

### 3. Comment System
- Add comments to blog posts (authenticated users)
- View all comments on a post (public access)
- Edit comments (comment authors only)
- Delete comments (comment authors only)
- Timestamps for creation and updates

### 4. Tagging System
- Add multiple tags to blog posts
- View posts by tag
- Tag-based filtering
- Tag display on post listings and details

### 5. Search Functionality
- Search posts by title, content, or tags
- Real-time search results
- Search bar in navigation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   \`\`\`bash
   cd django_blog
   \`\`\`

2. **Create a virtual environment**
   \`\`\`bash
   python -m venv venv
   \`\`\`

3. **Activate the virtual environment**
   - Windows:
     \`\`\`bash
     venv\Scripts\activate
     \`\`\`
   - macOS/Linux:
     \`\`\`bash
     source venv/bin/activate
     \`\`\`

4. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

5. **Run migrations**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

6. **Create a superuser (admin account)**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`
   Follow the prompts to create your admin account.

7. **Run the development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage Guide

### For Users

1. **Registration**
   - Click "Register" in the navigation
   - Fill in username, email, and password
   - Submit to create your account

2. **Creating Posts**
   - Login to your account
   - Click "New Post" in the navigation
   - Enter title, content, and tags (comma-separated)
   - Submit to publish

3. **Commenting**
   - Navigate to any blog post
   - Scroll to the comments section
   - Enter your comment and submit

4. **Searching**
   - Use the search bar in the navigation
   - Enter keywords to search titles, content, or tags
   - View filtered results

5. **Browsing by Tags**
   - Click any tag badge on a post
   - View all posts with that tag

### For Administrators

1. **Access Admin Panel**
   - Navigate to http://127.0.0.1:8000/admin/
   - Login with superuser credentials

2. **Manage Content**
   - View, edit, or delete posts and comments
   - Manage users and permissions
   - Monitor site activity

## Project Structure

\`\`\`
django_blog/
├── django_blog/          # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── blog/                # Blog application
│   ├── models.py        # Post and Comment models
│   ├── views.py         # View functions and classes
│   ├── forms.py         # Forms for posts, comments, users
│   ├── urls.py          # Blog URL patterns
│   ├── admin.py         # Admin configuration
│   └── templates/       # HTML templates
│       └── blog/
│           ├── base.html
│           ├── post_list.html
│           ├── post_detail.html
│           ├── post_form.html
│           ├── login.html
│           ├── register.html
│           └── ...
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
\`\`\`

## Models

### Post Model
- `title`: CharField (max 200 characters)
- `content`: TextField
- `published_date`: DateTimeField (auto-generated)
- `author`: ForeignKey to User
- `tags`: TaggableManager (many-to-many)

### Comment Model
- `post`: ForeignKey to Post
- `author`: ForeignKey to User
- `content`: TextField
- `created_at`: DateTimeField (auto-generated)
- `updated_at`: DateTimeField (auto-updated)

## Security Features

- CSRF protection on all forms
- Password hashing with Django's built-in algorithms
- User authentication required for creating/editing content
- Permission checks to ensure users can only edit their own content
- SQL injection protection through Django ORM

## Technologies Used

- **Backend**: Django 4.2
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Tagging**: django-taggit
- **Authentication**: Django's built-in auth system

## Future Enhancements

- Rich text editor for post content
- Image uploads for posts
- User avatars and extended profiles
- Email notifications for comments
- Social media sharing
- Post categories in addition to tags
- Draft posts functionality
- Comment moderation system

## Troubleshooting

### Common Issues

1. **Migration errors**
   \`\`\`bash
   python manage.py makemigrations --empty blog
   python manage.py migrate
   \`\`\`

2. **Static files not loading**
   \`\`\`bash
   python manage.py collectstatic
   \`\`\`

3. **Port already in use**
   \`\`\`bash
   python manage.py runserver 8080
   \`\`\`

## Contributing

This is a learning project for the ALX Django LearnLab. Feel free to fork and modify for your own learning purposes.

## License

This project is created for educational purposes as part of the ALX Django LearnLab curriculum.

## Repository

- **GitHub**: Alx_DjangoLearnLab
- **Directory**: django_blog

## Support

For issues or questions, please refer to the Django documentation at https://docs.djangoproject.com/
