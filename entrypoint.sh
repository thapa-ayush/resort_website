#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput 2>&1 || true

echo "Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 4 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    resort_website.wsgi:application
