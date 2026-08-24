#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.settings')
django.setup()

from django.conf import settings
from celery import Celery

print("=" * 60)
print("TESTING CELERY + REDIS CONNECTION")
print("=" * 60)

print(f"Broker URL: {settings.CELERY_BROKER_URL}")
print(f"Result Backend: {settings.CELERY_RESULT_BACKEND}")

# Create Celery app
app = Celery('test')
app.config_from_object('django.conf:settings', namespace='CELERY')

try:
    # Test connection
    conn = app.connection()
    conn.ensure_connection(max_retries=3)
    print("✅ Successfully connected to Redis!")
    conn.close()
except Exception as e:
    print(f"❌ Failed to connect to Redis: {e}")
    print("\nTroubleshooting steps:")
    print("1. Check if Redis is running: docker ps | grep redis")
    print("2. Check if port is mapped: docker port redis")
    print("3. Try: redis-cli -h localhost -p 6379 ping")