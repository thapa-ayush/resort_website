#!/usr/bin/env python
"""
Compress large images to fit Cloudinary free tier (10MB limit)
"""
import os
import sys
from pathlib import Path
from PIL import Image

MEDIA_FOLDER = Path(__file__).parent / 'media'
MAX_SIZE_MB = 9  # 9MB to be safe (10MB is limit)
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

def compress_image(image_path, target_size_bytes=MAX_SIZE_BYTES):
    """Compress an image to fit within target size."""
    try:
        img = Image.open(image_path)
        
        # Start with quality 95 and reduce until size is acceptable
        quality = 95
        while quality >= 20:
            # Save to bytes
            import io
            buffer = io.BytesIO()
            
            # Convert RGBA to RGB if needed (for JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            size = buffer.tell()
            
            if size <= target_size_bytes:
                # Save the compressed image
                with open(image_path, 'wb') as f:
                    f.write(buffer.getvalue())
                return True, size
            
            quality -= 5
        
        return False, buffer.tell()
    except Exception as e:
        return None, str(e)

# Process all files
print("🖼️ Compressing images for Cloudinary (max 10MB)...")
compressed = 0
failed = 0

for file_path in MEDIA_FOLDER.rglob('*'):
    if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
        size = file_path.stat().st_size
        
        if size > MAX_SIZE_BYTES:
            success, new_size = compress_image(file_path)
            if success:
                print(f"✅ {file_path.relative_to(MEDIA_FOLDER)} ({size/1024/1024:.1f}MB → {new_size/1024/1024:.1f}MB)")
                compressed += 1
            else:
                print(f"❌ {file_path.relative_to(MEDIA_FOLDER)}: {new_size}")
                failed += 1

print(f"\n✨ Compressed {compressed} images, {failed} failed")
print(f"Now run: python migrate_images.py")
