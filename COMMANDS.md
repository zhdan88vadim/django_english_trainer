
conda create -n english_trainer python=3.10 -y
conda activate english_trainer


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