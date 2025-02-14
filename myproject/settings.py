from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib.messages import constants as messages

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
DEBUG = os.getenv("DEBUG") == "True"
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    
    'django_cleanup',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'ckeditor',


    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'notification',
    'chat',
    'agora',
    'channels',
    'friend',
    'meetings',
    'bootstrap4',
    "crispy_forms",
    "crispy_bootstrap4",
    'exam',
    'file_converter',
    'support',
    "tailwind",
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
   
    
    
]

SITE_ID = 1



CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # Ensure this is included
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'myproject.urls'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'users/templates'),
                 os.path.join(BASE_DIR, 'exam/templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',#for google
    
]
SITE_ID = 1
WSGI_APPLICATION = 'myproject.wsgi.application'
ASGI_APPLICATION = "myproject.routing.application"

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and Media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Login and redirect settings
LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'


# settings.py (authentication settings)
# Add or update these settings
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'profile-list-view'  # or 'blog-home' depending on your preference
LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'account_login'


# CKEditor settings
CKEDITOR_CONFIGS = {
    'default': {
        'width': 'auto',
    },
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')
DEBUG = True

# Google reCAPTCHA

# Message tags for Bootstrap
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Channels settings
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

# Sites framework
SITE_ID = 1

# Social Account Providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '1019434985312-36nea89728f84ikv9e6e9kh9l3h9a49r.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Add this to your settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'meetings': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# settings.py
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'

# For development only
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# For production, set these to True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

CSP_FRAME_ANCESTORS = "'self' https://teams.microsoft.com https://*.cloud.microsoft https://app.diagrams.net"
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
