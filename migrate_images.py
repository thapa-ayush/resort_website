#!/usr/bin/env python
"""
Simple script to test Cloudinary credentials and migrate images
"""
import os
import sys
from pathlib import Path

# Read .env file directly and set environment variables
ENV_FILE = Path(__file__).parent / '.env'
print(f"Loading .env from: {ENV_FILE}")

if not ENV_FILE.exists():
    print(f"❌ .env file not found!")
    sys.exit(1)

with open(ENV_FILE, 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                os.environ[key] = value
                if 'CLOUDINARY' in key:
                    print(f"✓ Set {key} = {value[:20]}...")

# Verify they're in environ
print(f"\nVerifying environ:")
print(f"  CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET')}")
print(f"  CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY', 'NOT SET')[:10]}...")
print(f"  CLOUDINARY_API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET', 'NOT SET')[:10]}...")

# Now setup Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resort_website.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage

print(f"\n✓ Django configured")
print(f"\nDjango Settings Cloudinary:")
print(f"  Cloud Name: '{settings.CLOUDINARY_CLOUD_NAME}'")
print(f"  API Key: '{settings.CLOUDINARY_API_KEY}'")
print(f"  API Secret: '{settings.CLOUDINARY_API_SECRET}'")

if not settings.CLOUDINARY_CLOUD_NAME:
    print("\n❌ Cloudinary credentials not loaded in Django!")
    print(f"\nDEBUG - os.environ still has:")
    print(f"  CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    sys.exit(1)

print("\n✅ Credentials loaded successfully!")

# Migrate images
media_root = settings.MEDIA_ROOT
if media_root and os.path.exists(media_root):
    print(f"\n📁 Found media folder: {media_root}")
    uploaded = 0
    failed = 0
    for file_path in Path(media_root).rglob('*'):
        if file_path.is_file():
            rel_path = file_path.relative_to(media_root)
            try:
                with open(file_path, 'rb') as f:
                    url = default_storage.save(str(rel_path), f)
                print(f"✅ {rel_path} -> {url}")
                uploaded += 1
            except Exception as e:
                print(f"❌ {rel_path}: {e}")
                failed += 1
    print(f"\n✨ Done! Uploaded {uploaded} files, {failed} failed")
else:
    print(f"\n❌ No media folder found at {media_root}")
