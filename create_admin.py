#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resort_website.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser only if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@resort.com', 'admin123')
    print("✅ Superuser 'admin' created successfully!")
else:
    print("✅ Superuser 'admin' already exists")
