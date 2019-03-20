# Normally I would have used env level settings but this is just prototype....
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .default_settings import *


sentry_sdk.init(
    dsn="https://dc749c271d564a31a1b9444e27ca9f56@sentry.io/1402059",
    integrations=[DjangoIntegration()]
)


DEBUG = False

ALLOWED_HOSTS = [
    '188.166.173.237',
    'albert.visgean.me',
    'albertwaitfor.me',
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

FF_EXECUTABLE = '/home/albert/ff'
