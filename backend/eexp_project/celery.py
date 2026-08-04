from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eexp_project.settings')
app = Celery('eexp_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# ensure celery app is imported when Django starts
