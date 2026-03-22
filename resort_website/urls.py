"""
URL configuration for resort_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from main.admin import admin_site
from main.media_views import serve_media

urlpatterns = [
    # Custom Diamond Hill Resort admin
    path('admin/', admin_site.urls),
    
    # TinyMCE editor URLs
    path('tinymce/', include('tinymce.urls')),
    
    # Main app URLs
    path('', include('main.urls')),
    
    # Media files serving (only used with local storage, not Cloudinary)
    # When using Cloudinary, files are served directly via CDN
    re_path(r'^media/(?P<filepath>.*)$', serve_media, name='serve_media'),
]

# Add static file serving for development/local media storage
# When using Cloudinary storage, MEDIA_ROOT is None and this is skipped
if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files (needed for all environments)
# staticfiles/ directory is created during 'collectstatic' in Docker build
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

