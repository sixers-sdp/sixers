import os
import sys
import urllib.parse
import logging


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)



DEBUG = os.getenv('DEBUG_CONTROL') == 'true'

if DEBUG:
    API_URL = os.getenv('ALBERT_URL', 'http://127.0.0.1:8000/api/')
else:
    import sentry_sdk
    sentry_sdk.init("https://1502091405da4d9e9e6682f7caf67052@sentry.io/1408808")
    API_URL = os.getenv('ALBERT_URL', 'http://albert.visgean.me/api/')


API_CURRENT_PLAN_URL = urllib.parse.urljoin(API_URL, 'plans/latest/')
