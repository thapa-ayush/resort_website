"""
Debug views for troubleshooting Cloudinary and storage configuration.
"""

from django.http import JsonResponse
from django.conf import settings
import os
import traceback


def cloudinary_debug(request):
    """Debug endpoint - check Cloudinary configuration and settings."""
    try:
        # Get all Cloudinary settings
        debug_info = {
            'status': 'OK',
            'cloudinary_cloud_name': settings.CLOUDINARY_CLOUD_NAME or 'NOT SET',
            'cloudinary_api_key_set': bool(settings.CLOUDINARY_API_KEY),
            'cloudinary_api_secret_set': bool(settings.CLOUDINARY_API_SECRET),
            'default_file_storage': settings.DEFAULT_FILE_STORAGE,
            'media_url': settings.MEDIA_URL,
            'media_root': str(settings.MEDIA_ROOT),
            'env_cloudinary_cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET'),
            'env_api_key_set': bool(os.environ.get('CLOUDINARY_API_KEY')),
            'env_api_secret_set': bool(os.environ.get('CLOUDINARY_API_SECRET')),
        }
        
        return JsonResponse(debug_info)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


def image_urls_debug(request):
    """Debug endpoint - check image URLs in database."""
    try:
        import django
        from django.apps import apps
        
        debug_info = {'images': []}
        
        # Get Room model
        try:
            Room = apps.get_model('main', 'Room')
            rooms = Room.objects.all()[:2]
            for room in rooms:
                if room.image:
                    debug_info['images'].append({
                        'type': 'Room',
                        'name': room.title,
                        'image_name': room.image.name,
                        'image_url': room.image.url,
                    })
        except Exception as e:
            debug_info['room_error'] = str(e)
        
        # Get HeroSection model
        try:
            HeroSection = apps.get_model('main', 'HeroSection')
            slides = HeroSection.objects.all()[:2]
            for slide in slides:
                if slide.image:
                    debug_info['images'].append({
                        'type': 'Hero',
                        'name': slide.title,
                        'image_name': slide.image.name,
                        'image_url': slide.image.url,
                    })
        except Exception as e:
            debug_info['hero_error'] = str(e)
        
        # Get GalleryImage model
        try:
            GalleryImage = apps.get_model('main', 'GalleryImage')
            images = GalleryImage.objects.all()[:2]
            for img in images:
                if img.image:
                    debug_info['images'].append({
                        'type': 'Gallery',
                        'name': img.caption,
                        'image_name': img.image.name,
                        'image_url': img.image.url,
                    })
        except Exception as e:
            debug_info['gallery_error'] = str(e)
        
        return JsonResponse(debug_info)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)
