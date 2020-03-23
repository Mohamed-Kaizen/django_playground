#!/usr/bin bash

python manage.py makemigrations

echo "Migrate....."

python manage.py migrate
