#!/bin/sh

# Personal Preference to start fresh - You may comment
# Comment before your first production build (to retain migration history)
# echo "FLUSHING DATABASE"
# python manage.py flush --no-input
# echo "DELETING EXISTING MIGRATION FILES"
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -delete
# /Personal Preference to start fresh - You may comment

# echo "MAKING MIGRATION FILES"
# python manage.py makemigrations --noinput
echo "MIGRATING DATABASE"
python manage.py migrate --settings=config.settings.production --noinput
echo "SEEDING DATABASE | REFRESH"
python manage.py accounts_seed --settings=config.settings.production
echo "RUNNING ALL TEST CASES"
python manage.py test --settings=config.settings.production
echo "CREATING TEST SUPERUSER"
echo "from django.contrib.auth import get_user_model; user = get_user_model().objects.create_user(username='9999999999', email='webmaster@bit-boomer.com', password='DevTeam@123'); user.is_superuser=True; user.is_staff=True; user.save()" | python manage.py shell --settings=config.settings.production
echo "from django.contrib.auth import get_user_model; from django.contrib.auth.models import Group; manager_group, created = Group.objects.get_or_create(name='manager'); user = get_user_model().objects.create_user(username='9999999998', email='manager@bit-boomer.com', password='DevTeam@123'); manager_group.user_set.add(user); user.save()" | python manage.py shell --settings=config.settings.production

echo "STARTING WSGI GUNICORN SERVER WITH 2 WORKERS 4 THREADS (GTHREAD)"
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=2 --threads=4 --worker-class=gthread
