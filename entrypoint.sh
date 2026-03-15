#!/bin/bash

export DJANGO_SETTINGS_MODULE=resort_website.settings

echo "=== Starting Django Application ==="
echo "Python: $(python --version)"
echo "Django: $(python -c 'import django; print(django.__version__)')"
echo "PORT: ${PORT:-8000}"
echo "DEBUG: ${DEBUG:-False}"
echo ""

# Try to run migrations but don't fail if database isn't ready initially
echo "Attempting database migrations..."
python manage.py migrate --noinput 2>&1 || echo "Warning: Migrations failed, but continuing..."

# Collect static files (non-interactive)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear 2>&1 || echo "Warning: Static collection failed, but continuing..."

echo ""
echo "=== Starting Gunicorn ==="
echo "Binding to 0.0.0.0:${PORT:-8000}"
echo ""

# Start gunicorn with detailed output for debugging
python -m gunicorn \
    --workers 4 \
    --worker-class sync \
    --timeout 60 \
    --bind 0.0.0.0:${PORT:-8000} \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    resort_website.wsgi:application
