"""
Management command to migrate existing local media files to Cloudinary.
Usage: python manage.py migrate_to_cloudinary
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from pathlib import Path


class Command(BaseCommand):
    help = 'Migrate existing local media files to Cloudinary storage'

    def handle(self, *args, **options):
        # Check if Cloudinary credentials are configured
        if not settings.CLOUDINARY_CLOUD_NAME:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Cloudinary credentials not configured!\n'
                    'Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET\n'
                    'in your environment variables or .env file'
                )
            )
            return

        self.stdout.write(self.style.SUCCESS('🚀 Starting migration to Cloudinary...'))

        media_root = settings.MEDIA_ROOT
        if not media_root or not os.path.exists(media_root):
            self.stdout.write(self.style.WARNING('⚠️ No local media files found'))
            return

        # Recursively find and upload all media files
        uploaded_count = 0
        error_count = 0

        for file_path in Path(media_root).rglob('*'):
            if file_path.is_file():
                try:
                    # Get relative path from media root
                    relative_path = file_path.relative_to(media_root)
                    
                    # Read file and upload to Cloudinary
                    with open(file_path, 'rb') as f:
                        file_name = str(relative_path)
                        default_storage.save(file_name, f)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Uploaded: {relative_path}')
                    )
                    uploaded_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Failed to upload {file_path}: {str(e)}')
                    )
                    error_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'\n✨ Migration complete!\nUploaded: {uploaded_count}, Failed: {error_count}')
        )
