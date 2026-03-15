#!/bin/bash

export DJANGO_SETTINGS_MODULE=resort_website.settings

echo "=== Starting Django Application ==="
echo "Python: $(python --version)"
echo "PORT: ${PORT:-8000}"
echo ""

# Test that Django can load
echo "Testing Django configuration..."
python -c "import django; django.setup(); print('✓ Django loaded successfully')" || {
    echo "✗ Failed to load Django"
    exit 1
}

# Try to run migrations but don't fail if database isn't ready initially
echo "Attempting database migrations..."
python manage.py migrate --noinput 2>&1 || echo "⚠ Migrations skipped or failed"

# Collect static files (non-interactive)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear 2>&1 || echo "⚠ Static files collection skipped"

echo ""
echo "=== Starting Gunicorn on port ${PORT:-8000} ==="

# Start gunicorn
gunicorn \
    --workers 4 \
    --worker-class sync \
    --timeout 120 \
    --bind 0.0.0.0:${PORT:-8000} \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    resort_website.wsgi:application
