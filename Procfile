web: gunicorn resort_website.wsgi --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput
