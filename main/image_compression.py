"""
Django signals to automatically compress images before upload.
Handles large image files that exceed Cloudinary's 10MB free tier limit.
"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from PIL import Image
import io
import os

# Maximum file size: 9MB (safe margin below 10MB limit)
MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB in bytes


def compress_image(image_file, max_size_bytes=MAX_FILE_SIZE):
    """
    Compress an image file to fit within the size limit.
    
    Args:
        image_file: Django UploadedFile or File object
        max_size_bytes: Maximum file size in bytes
    
    Returns:
        Compressed ContentFile or original if already small
    """
    try:
        # Check original size
        if image_file.size and image_file.size <= max_size_bytes:
            return image_file
        
        # Open image
        image_file.seek(0)
        img = Image.open(image_file)
        
        # Convert RGBA to RGB if needed (for JPEG compatibility)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Determine format
        img_format = 'JPEG'
        if image_file.name.lower().endswith('.png'):
            img_format = 'PNG'
        
        # Compress with reducing quality until size is acceptable
        quality = 95
        compressed_buffer = None
        
        while quality >= 20:
            buffer = io.BytesIO()
            img.save(buffer, format=img_format, quality=quality, optimize=True)
            buffer.seek(0)
            size = buffer.getbuffer().nbytes
            
            if size <= max_size_bytes:
                compressed_buffer = buffer
                break
            
            quality -= 5
        
        if compressed_buffer is None:
            # If still too large, resize image
            max_dimension = 2000
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            quality = 85
            while quality >= 20:
                buffer = io.BytesIO()
                img.save(buffer, format=img_format, quality=quality, optimize=True)
                size = buffer.getbuffer().nbytes
                
                if size <= max_size_bytes:
                    compressed_buffer = buffer
                    break
                
                quality -= 5
        
        if compressed_buffer:
            compressed_buffer.seek(0)
            # Preserve original filename
            return ContentFile(compressed_buffer.read(), name=image_file.name)
        else:
            return image_file
    
    except Exception as e:
        # If compression fails, return original file
        print(f"Image compression failed: {e}")
        return image_file


def auto_compress_image_field(sender, instance, update_fields, **kwargs):
    """
    Signal handler to compress image fields before saving.
    Automatically applied to all models with ImageField.
    """
    from django.db.models import ImageField
    
    for field in sender._meta.get_fields():
        if isinstance(field, ImageField):
            image_field = getattr(instance, field.name, None)
            
            if image_field and hasattr(image_field, 'file') and image_field.file:
                # Check if it's a new upload (not just updating other fields)
                if not instance.pk or update_fields is None or field.name in update_fields:
                    compressed = compress_image(image_field.file)
                    if compressed != image_field.file:
                        setattr(instance, field.name, compressed)
                        print(f"✓ Auto-compressed {field.name} for {sender.__name__}")


# Register signal for all models that might need it
# We'll import this in apps.py and connect it to models
def connect_image_compression_signals():
    """Connect compression signals to all models with ImageFields."""
    from django.apps import apps
    
    for model in apps.get_models():
        from django.db.models import ImageField
        
        # Check if model has any ImageField
        has_image_field = any(
            isinstance(field, ImageField) 
            for field in model._meta.get_fields()
        )
        
        if has_image_field:
            pre_save.connect(auto_compress_image_field, sender=model, dispatch_uid=f'{model.__name__}_compress')
