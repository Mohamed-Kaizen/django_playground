web: gunicorn -w 4 django_playground.wsgi:application --log-file -
release: python manage.py migrate && python manage.py cleandata
