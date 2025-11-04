# LibraryProject

A Django project for managing a library system.

## Project Structure

This Django project follows the standard Django project structure:

- `manage.py`: A command-line utility that lets you interact with this Django project
- `LibraryProject/`: The main project package
  - `settings.py`: Configuration for the Django project
  - `urls.py`: The URL declarations for the project; a "table of contents" of your Django-powered site
  - `wsgi.py`: WSGI config for deployment
  - `asgi.py`: ASGI config for deployment

## Getting Started

### Prerequisites

- Python 3.x
- Django 5.2.5 or later

### Installation

1. Install Django (if not already installed):
   ```bash
   pip install django
   ```

2. Navigate to the project directory:
   ```bash
   cd LibraryProject
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Open your browser and navigate to `http://127.0.0.1:8000/` to view the default Django welcome page.

## Development Server

To run the development server:
```bash
python manage.py runserver
```

The server will start on `http://127.0.0.1:8000/` by default.

## Key Files

- `settings.py`: Contains all configuration settings for the Django project
- `urls.py`: Contains URL patterns that map URLs to views
- `manage.py`: Command-line utility for administrative tasks

