from urllib.parse import urlparse, parse_qsl

from .base import *

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

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