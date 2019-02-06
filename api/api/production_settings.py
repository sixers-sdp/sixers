# Normally I would have used env level settings but this is just prototype....

from .default_settings import *

DEBUG = False

ALLOWED_HOSTS = [
    '188.166.173.237',
    'albert.visgean.me',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')