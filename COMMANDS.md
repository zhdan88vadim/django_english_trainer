 docker compose restart celery

 docker compose up -d --build celery


python manage.py migrate django_celery_results
python manage.py migrate django_celery_beat  # If using beat




python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser  --username root --email a@a.com
pass: 123

celery -A server.celery worker --loglevel=info


python manage.py runserver 192.168.0.254:8090


docker compose up frontend --build


## URLs

http://localhost:3000/generate
http://localhost:8090/admin/django_celery_results/taskresult/
http://localhost:5555/flower/workers






pip check


# Step 1: Uninstall all packages
pip freeze | xargs pip uninstall -y

# Step 2: Install from requirements.txt
pip install -r requirements.txt








python manage.py runserver 8090
docker compose up redis db -d
docker compose up db 




## developing

http://localhost:3000/?category_id=1

npm run start

docker compose up






conda create -n english_trainer python=3.10 -y
conda activate english_trainer


http://127.0.0.1:8090/api-auth/login/?next=/

http://127.0.0.1:8090/admin/video_generator/text/add/



pip install django
pip install psycopg2-binary
pip install python-decouple



django-admin --version

django-admin startproject video_generator .

python manage.py migrate


python manage.py createsuperuser


# RUN

python manage.py runserver 8090

http://127.0.0.1:8090/admin/ 




# DEBUG

## get correct python path

bash
# Activate your conda environment
conda activate english_trainer

# Find the Python path
which python




pip install django-allauth



http://127.0.0.1:8090/accounts/signup/


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


pip install django-celery-results

python manage.py migrate django_celery_results

Step 5: Verify Setup
python
# In Django shell
python manage.py shell

>>> from celery import current_app
>>> current_app.conf.result_backend
'django-db'






pip freeze > requirements.txt





apt-get update && apt-get install -y nano






!!!!!
# Reconnect to the 'postgres' database instead
docker exec -it <container_name> psql -U trainer_user -d postgres

# Now drop the database
DROP DATABASE english_trainer;




!!!!!
docker compose exec db psql -U trainer_user -d postgres -c "CREATE DATABASE english_trainer;"



