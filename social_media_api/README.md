# Social Media API

A comprehensive Django REST API for a social media platform with user authentication, posts, comments, likes, follows, and notifications.

## Features

- **User Authentication**: Custom user model with registration, login, and token-based authentication
- **User Profiles**: Bio, profile pictures, and follower/following relationships
- **Posts**: Create, read, update, and delete posts
- **Comments**: Comment on posts with full CRUD operations
- **Likes**: Like and unlike posts
- **Follow System**: Follow/unfollow users and view personalized feed
- **Notifications**: Real-time notifications for likes, comments, and new followers
- **Pagination**: Efficient data loading with pagination
- **Search & Filtering**: Search posts by title and content

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd social_media_api
   \`\`\`

2. **Create a virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Run migrations**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

5. **Create a superuser (optional)**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

6. **Run the development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication

- `POST /api/accounts/register/` - Register a new user
- `POST /api/accounts/login/` - Login and get authentication token
- `GET /api/accounts/profile/` - Get current user profile
- `PUT /api/accounts/profile/` - Update current user profile
- `GET /api/accounts/users/<id>/` - Get user profile by ID

### Follow System

- `POST /api/accounts/follow/<user_id>/` - Follow a user
- `POST /api/accounts/unfollow/<user_id>/` - Unfollow a user

### Posts

- `GET /api/posts/posts/` - List all posts
- `POST /api/posts/posts/` - Create a new post
- `GET /api/posts/posts/<id>/` - Get post details
- `PUT /api/posts/posts/<id>/` - Update a post
- `DELETE /api/posts/posts/<id>/` - Delete a post
- `GET /api/posts/posts/feed/` - Get personalized feed from followed users
- `POST /api/posts/posts/<id>/like/` - Like a post
- `POST /api/posts/posts/<id>/unlike/` - Unlike a post

### Comments

- `GET /api/posts/comments/` - List all comments
- `POST /api/posts/comments/` - Create a new comment
- `GET /api/posts/comments/<id>/` - Get comment details
- `PUT /api/posts/comments/<id>/` - Update a comment
- `DELETE /api/posts/comments/<id>/` - Delete a comment
- `GET /api/posts/comments/?post=<post_id>` - Get comments for a specific post

### Notifications

- `GET /api/notifications/` - List all notifications
- `GET /api/notifications/unread/` - Get unread notifications
- `POST /api/notifications/<id>/mark_as_read/` - Mark notification as read
- `POST /api/notifications/mark_all_as_read/` - Mark all notifications as read

## Authentication

This API uses Token Authentication. To authenticate:

1. Register or login to get your token
2. Include the token in the Authorization header for all requests:
   \`\`\`
   Authorization: Token <your-token-here>
   \`\`\`

## Testing with Postman

### 1. Register a User

**Request:**
\`\`\`
POST http://localhost:8000/api/accounts/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "bio": "Hello, I'm a test user!"
}
\`\`\`

**Response:**
\`\`\`json
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "bio": "Hello, I'm a test user!",
        "followers_count": 0,
        "following_count": 0
    },
    "token": "your-auth-token-here",
    "message": "User registered successfully"
}
\`\`\`

### 2. Create a Post

**Request:**
\`\`\`
POST http://localhost:8000/api/posts/posts/
Authorization: Token <your-token>
Content-Type: application/json

{
    "title": "My First Post",
    "content": "This is the content of my first post!"
}
\`\`\`

### 3. Like a Post

**Request:**
\`\`\`
POST http://localhost:8000/api/posts/posts/1/like/
Authorization: Token <your-token>
\`\`\`

### 4. Follow a User

**Request:**
\`\`\`
POST http://localhost:8000/api/accounts/follow/2/
Authorization: Token <your-token>
\`\`\`

### 5. Get Feed

**Request:**
\`\`\`
GET http://localhost:8000/api/posts/posts/feed/
Authorization: Token <your-token>
\`\`\`

## Project Structure

\`\`\`
social_media_api/
├── accounts/              # User authentication and profiles
│   ├── models.py         # CustomUser model
│   ├── serializers.py    # User serializers
│   ├── views.py          # Authentication views
│   └── urls.py           # Account routes
├── posts/                # Posts, comments, and likes
│   ├── models.py         # Post, Comment, Like models
│   ├── serializers.py    # Post serializers
│   ├── views.py          # Post viewsets
│   ├── permissions.py    # Custom permissions
│   ├── signals.py        # Notification signals
│   └── urls.py           # Post routes
├── notifications/        # Notification system
│   ├── models.py         # Notification model
│   ├── serializers.py    # Notification serializers
│   ├── views.py          # Notification views
│   └── urls.py           # Notification routes
├── social_media_api/     # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # This file
\`\`\`

## Models Overview

### CustomUser
- Extends Django's AbstractUser
- Fields: bio, profile_picture, followers (ManyToMany)
- Methods: follow(), unfollow(), is_following()

### Post
- Fields: author, title, content, created_at, updated_at
- Properties: likes_count, comments_count

### Comment
- Fields: post, author, content, created_at, updated_at

### Like
- Fields: user, post, created_at
- Unique constraint: (user, post)

### Notification
- Fields: recipient, actor, verb, target (GenericForeignKey), read, timestamp
- Automatically created for likes, comments, and follows

## Development

### Running Tests
\`\`\`bash
python manage.py test
\`\`\`

### Creating Migrations
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### Accessing Admin Panel
1. Create a superuser: `python manage.py createsuperuser`
2. Visit: `http://localhost:8000/admin/`

## Production Deployment

See the deployment documentation in the project for instructions on deploying to production environments like Heroku, AWS, or DigitalOcean.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
