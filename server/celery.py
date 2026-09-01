import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.settings')

app = Celery('english_project')

# Use Django settings for Celery configuration with namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Debug: Print broker URL on startup
print(f"Celery broker URL: {app.conf.broker_url}")


# Optional: Debug
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    