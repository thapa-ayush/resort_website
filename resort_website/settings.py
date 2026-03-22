"""
Django settings for resort_website project.

Generated for Diamond Hill Resort project.
For more information, visit: https://docs.djangoproject.com/en/4.2/topics/settings/

Settings are configured to use environment variables for sensitive data.
Copy .env.example to .env and fill in the values.
"""

import os
import sys
from pathlib import Path
from decouple import config, Csv
import dj_database_url
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Load from environment, with fallback for development
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-dev-key-change-in-production'
)

# SECURITY WARNING: don't run with debug turned on in production!
# Default to False for security (can be overridden with DEBUG=True environment variable)
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts for CSRF protection
# Dynamically configured with Railway, Heroku, and other platform support
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1,resortwebsite-production.up.railway.app,.up.railway.app,.railway.app,.herokuapp.com',
    cast=Csv()
)

# Application definition
INSTALLED_APPS = [
    # Django admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'django_extensions',  # Optional: for shell_plus and other utilities
    'tinymce',  # Rich text editor
    'cloudinary_storage',  # Cloudinary storage backend
    'cloudinary',  # Cloudinary API
    
    # Local apps
    'main.apps.MainConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'resort_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'resort_website.wsgi.application'

# Database configuration
# Support for DATABASE_URL environment variable (Railway, Heroku, etc.)
# Fallback to SQLite for local development

if 'DATABASE_URL' in os.environ:
    # Production: Use DATABASE_URL (e.g., PostgreSQL on Railway)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
            'NAME': str(BASE_DIR / config('DB_NAME', default='db.sqlite3')),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'main' / 'static',
]

# Media files (User uploads) - Using Cloudinary
# https://docs.djangoproject.com/en/4.2/topics/files/

# Cloudinary Configuration - Load from environment variables
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default='')
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default='')
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default='')

# Cloudinary Storage Configuration (required by django-cloudinary-storage)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
    'STATICFILES_STORAGE': 'cloudinary_storage.storage.StaticHashedCloudinaryStorage',
}

# Configure cloudinary library with credentials
if CLOUDINARY_CLOUD_NAME:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True,
    )

# Use Cloudinary for media storage (always, config handles empty credentials)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = None  # Not used with Cloudinary storage

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security Settings (For Production)
# https://docs.djangoproject.com/en/4.2/topics/security/

# HTTPS only - DISABLED for Railway (uses reverse proxy with SECURE_PROXY_HEADER)
SECURE_SSL_REDIRECT = False

# Trust X-Forwarded-Proto header from reverse proxy (Railway)
SECURE_PROXY_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Secure cookies - DISABLED for Railway proxy
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# CSRF settings
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_AGE = 31449600  # 1 year
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://resortwebsite-production.up.railway.app',
    'https://*.up.railway.app',
    'https://*.railway.app',
]

# Clickjacking protection
X_FRAME_OPTIONS = 'DENY'

# Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'form-action': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'code.jquery.com'),
    'style-src': ("'self'", "'unsafe-inline'", 'cdn.jsdelivr.net'),
    'img-src': ("'self'", 'data:', '*'),
    'font-src': ("'self'", 'data:', 'fonts.googleapis.com', 'fonts.gstatic.com'),
}

# Email Configuration (for development, uses console backend)
# https://docs.djangoproject.com/en/4.2/topics/email/
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)

# Optional: Configure SMTP for production
# EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
# EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@diamondhillresort.com')

# Payment Gateway Keys (from environment)
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')
KHALTI_PUBLIC_KEY = config('KHALTI_PUBLIC_KEY', default='')
KHALTI_SECRET_KEY = config('KHALTI_SECRET_KEY', default='')
ESEWA_MERCHANT_CODE = config('ESEWA_MERCHANT_CODE', default='')

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# TinyMCE Configuration for Rich Text Editing
TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': '100%',
    'plugins': 'link image media table code help wordcount insertdatetime autolink lists advlist preview',
    'toolbar': (
        'formatselect | bold italic underline strikethrough | '
        'bullist numlist blockquote | link image media | '
        'alignleft aligncenter alignright | '
        'undo redo | code | removeformat | help'
    ),
    'menubar': 'file edit view insert format tools table',
    'branding': False,
    'promotion': False,
    'statusbar': True,
    'block_formats': 'Paragraph=p;Heading 1=h1;Heading 2=h2;Heading 3=h3;Heading 4=h4;Preformatted=pre',
    'fontsize_formats': '8pt 10pt 12pt 14pt 18pt 24pt 36pt',
    'relative_urls': False,
}
