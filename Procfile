release: python manage.py migrate
web: gunicorn -w 4 django_playground.wsgi:application
