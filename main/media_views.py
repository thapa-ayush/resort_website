from django.http import FileResponse, HttpResponseNotFound, HttpResponseRedirect
from django.conf import settings
import os

def serve_media(request, filepath):
    """
    Serve media files from MEDIA_ROOT directory (local storage only).
    When using Cloudinary storage, this view is not needed as Cloudinary
    serves files directly via CDN.
    """
    # If using Cloudinary, redirect to Cloudinary URL
    if settings.DEFAULT_FILE_STORAGE == 'cloudinary_storage.storage.MediaCloudinaryStorage':
        # Cloudinary URLs are served directly; this view shouldn't be called
        return HttpResponseNotFound("File not found - using Cloudinary storage")
    
    # Only serve local files if MEDIA_ROOT is configured (local development)
    if settings.MEDIA_ROOT is None:
        return HttpResponseNotFound("Media storage not configured")
    
    file_path = os.path.join(settings.MEDIA_ROOT, filepath)
    
    # Security check: ensure the path is within MEDIA_ROOT
    if not os.path.abspath(file_path).startswith(os.path.abspath(settings.MEDIA_ROOT)):
        return HttpResponseNotFound("File not found")
    
    # Check if file exists
    if not os.path.exists(file_path):
        return HttpResponseNotFound("File not found")
    
    # Serve the file
    try:
        return FileResponse(open(file_path, 'rb'), as_attachment=False)
    except FileNotFoundError:
        return HttpResponseNotFound("File not found")
