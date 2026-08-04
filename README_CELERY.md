# README additions: Celery run instructions

To run Celery locally (for the background CSV importer):

1. Start Redis (docker-compose up -d redis) or have Redis running at redis://localhost:6379/0
2. Start the Django dev server (in backend/): python manage.py runserver
3. In another terminal, start the Celery worker from repository root:
   celery -A eexp_project worker -l info

The CSV import task will be enqueued when you call the start import endpoint:
POST /api/upload/csv/{upload_id}/start/

