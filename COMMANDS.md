python manage.py makemigrations

python manage.py migrate

celery -A celery_app worker --loglevel=info


python manage.py runserver 8080
docker compose up redis db -d
docker compose up db 








conda create -n english_trainer python=3.10 -y
conda activate english_trainer


http://127.0.0.1:8080/api-auth/login/?next=/

http://127.0.0.1:8080/admin/video_generator/text/add/



pip install django
pip install psycopg2-binary
pip install python-decouple



django-admin --version

django-admin startproject video_generator .

python manage.py migrate


python manage.py createsuperuser


# RUN

python manage.py runserver 8080

http://127.0.0.1:8080/admin/ 




# DEBUG

## get correct python path

bash
# Activate your conda environment
conda activate english_trainer

# Find the Python path
which python




pip install django-allauth



http://127.0.0.1:8080/accounts/signup/


pip install djangorestframework


python manage.py createsuperuser --username admin --email admin@example.com




python manage.py makemigrations video_generator

python manage.py migrate video_generator






pip install django-cors-headers





# debug


1. Check your current Celery configuration
First, check what broker URL Celery is using:

bash
# Check from Django shell
python manage.py shell
python
from django.conf import settings
print(settings.CELERY_BROKER_URL)





