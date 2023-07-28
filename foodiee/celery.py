from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodiee.settings')
app = Celery('foodiee', include=['authentication.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
