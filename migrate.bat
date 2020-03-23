@echo off
REM run python manage.py makemigration and migrate
echo "Make migrations...."
python manage.py makemigrations
echo "migrate....."
python manage.py migrate
