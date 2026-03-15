from django.http import FileResponse, HttpResponseNotFound
from django.conf import settings
import os

def serve_media(request, filepath):
    """
    Serve media files from MEDIA_ROOT directory.
    Works in both development and production.
    """
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
