"""
Management command to migrate existing image files from local storage to Cloudinary.

This uploads all existing local images to Cloudinary using the Cloudinary API.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
import cloudinary.uploader
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Upload existing local image files to Cloudinary'

    def handle(self, *args, **options):
        # Check if Cloudinary is configured
        if not settings.CLOUDINARY_CLOUD_NAME:
            self.stdout.write(
                self.style.ERROR('Cloudinary not configured. Set CLOUDINARY_CLOUD_NAME environment variable.')
            )
            return

        self.stdout.write(self.style.SUCCESS('Starting image upload to Cloudinary...'))
        
        # Models with image fields
        models_to_migrate = [
            ('main', 'Room', 'image'),
            ('main', 'RoomImage', 'image'),
            ('main', 'GalleryImage', 'image'),
            ('main', 'BlogPost', 'featured_image'),
            ('main', 'HeroSection', 'image'),
            ('main', 'About', 'image'),
        ]
        
        total_uploaded = 0
        media_root = settings.MEDIA_ROOT
        
        for app_label, model_name, field_name in models_to_migrate:
            try:
                Model = apps.get_model(app_label, model_name)
                instances = Model.objects.exclude(**{f'{field_name}': ''}).exclude(**{f'{field_name}__isnull': True})
                
                if not instances.exists():
                    self.stdout.write(f'  {model_name}: No images to upload')
                    continue
                
                uploaded = 0
                for instance in instances:
                    field = getattr(instance, field_name, None)
                    if field and field.name:
                        local_path = os.path.join(media_root, field.name)
                        
                        # Check if file exists locally
                        if not os.path.exists(local_path):
                            self.stdout.write(
                                self.style.WARNING(
                                    f'    ! {model_name}.{instance.id}: File not found: {local_path}'
                                )
                            )
                            continue
                        
                        try:
                            # Upload to Cloudinary with the same path as the filename
                            public_id = field.name.rsplit('.', 1)[0]  # Remove extension for public_id
                            
                            result = cloudinary.uploader.upload(
                                local_path,
                                public_id=public_id,
                                overwrite=True,
                                resource_type='auto',
                            )
                            
                            uploaded += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'    ✓ {model_name}: {field.name}')
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'    ✗ {model_name}.{instance.id}: {str(e)}'
                                )
                            )
                
                if uploaded > 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'  {model_name}: Uploaded {uploaded} images')
                    )
                    total_uploaded += uploaded
                    
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'  Error with {model_name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Upload complete! Total images uploaded: {total_uploaded}')
        )
