"""
App configuration for the main application.
"""
from django.apps import AppConfig


class MainConfig(AppConfig):
    """Configuration for the main app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    def ready(self):
        """Initialize app signals and handlers."""
        from .image_compression import connect_image_compression_signals
        connect_image_compression_signals()
