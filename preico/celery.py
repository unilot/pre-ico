from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from .settings import DEBUG

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'preico.settings')

app = Celery('preico')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    if DEBUG:
        print('Request: {0!r}'.format(self.request))
