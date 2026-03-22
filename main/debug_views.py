"""
Debug views for troubleshooting Cloudinary and storage configuration.
Only accessible in development or with debug key in production.
"""

from django.http import JsonResponse
from django.conf import settings
import cloudinary
import os


def cloudinary_debug(request):
    """Debug endpoint to check Cloudinary configuration."""
    debug_info = {
        'cloudinary_configured': bool(settings.CLOUDINARY_CLOUD_NAME),
        'cloud_name': settings.CLOUDINARY_CLOUD_NAME or 'NOT SET',
        'api_key_set': bool(settings.CLOUDINARY_API_KEY),
        'api_secret_set': bool(settings.CLOUDINARY_API_SECRET),
        'default_file_storage': settings.DEFAULT_FILE_STORAGE,
        'media_url': settings.MEDIA_URL,
        'media_root': str(settings.MEDIA_ROOT) if settings.MEDIA_ROOT else None,
        'cloudinary_config': {
            'cloud_name': cloudinary.config().cloud_name or 'NOT SET',
            'api_key_set': bool(cloudinary.config().api_key),
            'api_secret_set': bool(cloudinary.config().api_secret),
        },
        'environment_variables': {
            'CLOUDINARY_CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET'),
            'CLOUDINARY_API_KEY': 'SET' if os.environ.get('CLOUDINARY_API_KEY') else 'NOT SET',
            'CLOUDINARY_API_SECRET': 'SET' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET',
        }
    }
    
    return JsonResponse(debug_info, indent=2)


def image_urls_debug(request):
    """Debug endpoint to check image URLs for all models."""
    from main.models import Room, GalleryImage, BlogPost, HeroSection, AboutSection
    
    debug_info = {
        'rooms': [],
        'gallery_images': [],
        'blog_posts': [],
        'hero_slides': [],
        'about_section': None,
    }
    
    # Check Rooms
    try:
        for room in Room.objects.all():
            debug_info['rooms'].append({
                'title': room.title,
                'has_image': bool(room.image),
                'image_field_type': str(type(room.image)),
                'image_url': room.image.url if room.image else None,
                'image_name': room.image.name if room.image else None,
            })
    except Exception as e:
        debug_info['rooms'].append({'error': str(e)})
    
    # Check Gallery Images
    try:
        for image in GalleryImage.objects.all()[:3]:  # First 3
            debug_info['gallery_images'].append({
                'caption': image.caption,
                'has_image': bool(image.image),
                'image_url': image.image.url if image.image else None,
                'image_name': image.image.name if image.image else None,
            })
    except Exception as e:
        debug_info['gallery_images'].append({'error': str(e)})
    
    # Check Blog Posts
    try:
        for post in BlogPost.objects.all()[:3]:  # First 3
            debug_info['blog_posts'].append({
                'title': post.title,
                'has_image': bool(post.image),
                'image_url': post.image.url if post.image else None,
                'image_name': post.image.name if post.image else None,
            })
    except Exception as e:
        debug_info['blog_posts'].append({'error': str(e)})
    
    # Check Hero Slides
    try:
        for slide in HeroSection.objects.all()[:3]:  # First 3
            debug_info['hero_slides'].append({
                'title': slide.title,
                'has_image': bool(slide.image),
                'image_url': slide.image.url if slide.image else None,
                'image_name': slide.image.name if slide.image else None,
            })
    except Exception as e:
        debug_info['hero_slides'].append({'error': str(e)})
    
    # Check About Section
    try:
        about = AboutSection.objects.first()
        if about:
            debug_info['about_section'] = {
                'has_image': bool(about.image),
                'image_url': about.image.url if about.image else None,
                'image_name': about.image.name if about.image else None,
            }
    except Exception as e:
        debug_info['about_section'] = {'error': str(e)}
    
    return JsonResponse(debug_info, indent=2)
