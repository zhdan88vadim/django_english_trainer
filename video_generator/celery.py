import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_generator.settings')

app = Celery('english_project')

# Force Redis configuration (override any other settings)
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# read from config
# app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Debug: Print broker URL on startup
print(f"✅ Celery broker URL: {app.conf.broker_url}")


# Optional: Debug
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    