from .base import *

DEBUG=True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'test_db.sqlite3'),
    }
}