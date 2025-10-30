# Django Setup Instructions

## Prerequisites
- Python 3.8 or higher installed
- pip package manager available

## Installation Steps

### 1. Install Django
\`\`\`bash
pip install django
\`\`\`

### 2. Project Structure
The LibraryProject has been created with the following structure:
- `manage.py`: Django command-line utility
- `LibraryProject/`: Main project configuration directory
- `bookshelf/`: Django app for managing books

### 3. Run Migrations
\`\`\`bash
cd LibraryProject
python manage.py migrate
\`\`\`

### 4. Create a Superuser (Admin Account)
\`\`\`bash
python manage.py createsuperuser
\`\`\`
Follow the prompts to create your admin account.

### 5. Start the Development Server
\`\`\`bash
python manage.py runserver
\`\`\`

### 6. Access the Application
- **Django Welcome Page**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/

## Project Configuration

### settings.py
- Database: SQLite (db.sqlite3)
- Installed Apps: admin, auth, contenttypes, sessions, messages, staticfiles, bookshelf
- Debug Mode: Enabled (change to False in production)

### Database
- Engine: Django ORM with SQLite
- Migrations: Located in `bookshelf/migrations/`

## Useful Commands

\`\`\`bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Access Django shell for interactive operations
python manage.py shell

# Run tests
python manage.py test

# Create a superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Collect static files
python manage.py collectstatic
