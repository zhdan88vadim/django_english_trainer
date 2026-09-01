from pathlib import Path
from decouple import config


# Celery Configuration
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
# CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')  # for local dev

# Result backend - using Django database
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')

# Serialization settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Timezone settings
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# Task execution settings
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_RESULT_EXPIRES = 86400  # 24 hours
CELERY_RESULT_EXTENDED = True

# Result expiration
CELERY_RESULT_EXPIRES = 3600  # 1 hour

# Broker connection settings
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 10

# Additional Celery settings
CELERY_ACKS_LATE = True
CELERY_REJECT_ON_WORKER_LOST = True