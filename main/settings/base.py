"""
Django settings for Canopy code challenge.
"""
import os
import re

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', 'gul=%kxw#3*wqeul5_9wnd-j959gah8s)wxcqgplg5=w14curt')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('DEBUG') == 'false' else True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = ALLOWED_HOSTS.split(',') if ALLOWED_HOSTS else []

# STATIC FILES
STATIC_ROOT = os.path.join(BASE_DIR, "../assets/")
STATIC_URL = "/static/"

# DOMAINS and BASICS
APP_DOMAIN = os.getenv('APP_DOMAIN', 'canopy-challenge.com')

SITE_ID = int(os.getenv('SITE_ID', 1))
SITES = {
    'dev': {
        'id': 1,
        'domain': '127.0.0.1:8000',
    },
}

ADMINS = [('Susel', 'suselrd@gmail.com')]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_REGEX_WHITELIST = (
    r'^(\w+?://)?127.0.0.1(:\d{1,5})?$',
    r'^(\w+?://)?localhost(:\d{1,5})?$',
    r'^(\w+?://)?%s$' % re.escape(APP_DOMAIN),
)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'rooms',
    'movies',
    'schedule',
    'tickets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
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

WSGI_APPLICATION = 'main.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'canopy',
        'USER': os.getenv('POSTGRES_USER') or 'postgres',
        'PASSWORD': os.getenv('POSTGRES_PASSWORD') or 'postgres',
        'PORT': '5432',
    }
}

# Logging
LOG_HANDLERS = {
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
    }
}
ALL_HANDLERS = list(LOG_HANDLERS.keys())
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': LOG_HANDLERS,
    'loggers': {
        '': {
            'handlers': ALL_HANDLERS,
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ALL_HANDLERS,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False
        },
        'stripe': {
            'handlers': ALL_HANDLERS,
            'level': os.getenv('STRIPE_LOG_LEVEL', 'ERROR'),
            'propagate': False
        },
        'celery': {
            'handlers': ALL_HANDLERS,
            'level': os.getenv('CELERY_LOG_LEVEL', 'ERROR'),
            'propagate': False
        }
    },
}

# Internationalization
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en-US'
LANGUAGES = [
    ('en', _('English')),
]

# Timezones
USE_TZ = True
TIME_ZONE = 'UTC'

# API
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    # for request a specific version send request header: Accept: application/json; version=1.0
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
        'user': '600/minute'
    },
    'DATE_FORMAT': '%a, %d %b %Y',
    'DATETIME_FORMAT': '%a, %d %b %Y %I:%M:%S %p'
}
