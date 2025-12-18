from urllib.parse import urlparse, parse_qsl

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


# Replace the DATABASES section of your settings.py with this
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': int(os.environ['DB_PORT']),
    }
}

STATIC_URL = "static/"
STATIC_ROOT = "staticfiles/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]