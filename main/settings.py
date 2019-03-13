import os
import sys
import urllib.parse
import logging

sys.path.append(os.path.abspath('..'))



logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

DEBUG = os.getenv('DEBUG_CONTROL') == 'true'

AUTH_TOKEN = os.getenv('AUTH_TOKEN', '')
assert len(AUTH_TOKEN) > 3, "You must set up auth token variable!"

if DEBUG:
    API_URL = os.getenv('ALBERT_URL', 'http://127.0.0.1:8000/api/')
else:
    import sentry_sdk
    sentry_sdk.init("https://1502091405da4d9e9e6682f7caf67052@sentry.io/1408808")
    API_URL = os.getenv('ALBERT_URL', 'http://albert.visgean.me/api/')


API_CURRENT_PLAN_URL = urllib.parse.urljoin(API_URL, 'plans/latest/')
API_DETAIL_PLAN_URL = urllib.parse.urljoin(API_URL, 'plans/{0}/')

AUTH_HEADERS = {'Authorization': 'Token {0}'.format(AUTH_TOKEN)}

API_LOCATION = urllib.parse.urljoin(API_URL, 'location/')
API_DETAIL_ORDER_URL = urllib.parse.urljoin(API_URL, 'orders/{0}/')
