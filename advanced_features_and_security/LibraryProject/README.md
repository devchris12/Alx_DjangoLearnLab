# Permissions & Groups (library app)

## Custom Permissions
Defined on `library.Book` (Meta.permissions):
- `library.can_view`
- `library.can_create`
- `library.can_edit`
- `library.can_delete`

## Groups (create in /admin/)
Create three groups and assign permissions:
- **Viewers** → `can_view`
- **Editors** → `can_view`, `can_create`, `can_edit`
- **Admins**  → `can_view`, `can_create`, `can_edit`, `can_delete`

## Enforced in Views
- `/books/` → requires `library.can_view`
- `/books/create/` → requires `library.can_create` (POST with `title`)
- `/books/<id>/edit/` → requires `library.can_edit` (POST with `title`)
- `/books/<id>/delete/` → requires `library.can_delete` (POST)

## How to Test
```bash
python manage.py makemigrations library
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
