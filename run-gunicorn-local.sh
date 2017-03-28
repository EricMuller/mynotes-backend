# export DJANGO_DEBUG=false
python manage.py collectstatic --noinput
gunicorn -w 8 --threads 9 --env DJANGO_SETTINGS_MODULE=config.settings.local config.wsgi 
