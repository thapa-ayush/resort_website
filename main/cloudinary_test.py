"""
Debug view to test Cloudinary configuration.
Only available in DEBUG mode.
"""
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
import cloudinary


@require_http_methods(["GET"])
def test_cloudinary(request):
    """Test if Cloudinary is properly configured."""
    
    if not settings.DEBUG:
        return JsonResponse({'error': 'Only available in DEBUG mode'}, status=403)
    
    # Check environment variables
    cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', '')
    api_key = getattr(settings, 'CLOUDINARY_API_KEY', '')
    api_secret = getattr(settings, 'CLOUDINARY_API_SECRET', '')
    
    # Check if credentials are loaded
    has_credentials = bool(cloud_name and api_key)
    
    # Get cloudinary config
    cloudinary_config = cloudinary.config()
    
    return JsonResponse({
        'debug_mode': settings.DEBUG,
        'storage_backend': settings.DEFAULT_FILE_STORAGE,
        'cloudinary_config': {
            'cloud_name': cloud_name or 'NOT SET',
            'api_key': (api_key[:10] + '...') if api_key else 'NOT SET',
            'api_secret': (api_secret[:10] + '...') if api_secret else 'NOT SET',
            'has_credentials': has_credentials,
        },
        'cloudinary_lib_config': {
            'cloud_name': cloudinary_config.cloud_name or 'NOT SET',
            'api_key': cloudinary_config.api_key or 'NOT SET',
        },
        'media_url': settings.MEDIA_URL,
        'media_root': str(settings.MEDIA_ROOT) if settings.MEDIA_ROOT else 'None (Cloudinary)',
    }, indent=2)
