# E-EXP: School Management System (Django MVP)

This repository contains a scaffold for a School Management System MVP built with Django and Django REST Framework.

Development quickstart (local):

1. Install Python 3.10+ and pip.
2. python -m venv .venv && source .venv/bin/activate
3. pip install -r requirements.txt
4. cd backend
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver

Notes:
- This scaffold uses SQLite for local development. For production, switch to PostgreSQL and configure via environment variables.
- CSV template for student master upload is in docs/student_master_template.csv

What's included in this branch:
- Minimal Django project (backend/) with a `school` app
- Core models: custom User, School, ClassRoom, Student, Parent, Subject, Mark, CSVUpload
- Admin registrations
- Basic CSV upload API endpoint (saves uploaded CSV as CSVUpload record)

Next steps I will take after your review:
- Implement full CSV validation & dry-run
- Add background import with Celery
- Add StudentID generator and automatic user creation with secure temporary passwords
- Add React frontend or expand Django admin UX

If you want me to continue, say "Continue scaffolding CSV import and StudentID generation".
