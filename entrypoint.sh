#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=resort_website.settings

echo "=== Starting Django Application ==="
echo "PORT: ${PORT:-8000}"
echo "DEBUG: ${DEBUG:-False}"
echo ""

# Try to run migrations but don't fail if database isn't ready initially
echo "Attempting database migrations..."
python manage.py migrate --noinput || true

# Collect static files (non-interactive)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true

echo ""
echo "=== Starting Gunicorn ==="
echo "Binding to 0.0.0.0:${PORT:-8000}"
echo ""

# Start gunicorn with detailed output for debugging
exec gunicorn \
    --workers 4 \
    --worker-class sync \
    --timeout 60 \
    --bind 0.0.0.0:${PORT:-8000} \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    resort_website.wsgi:application
