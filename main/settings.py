import os
import urllib.parse

import sentry_sdk
sentry_sdk.init("https://1502091405da4d9e9e6682f7caf67052@sentry.io/1408808")


API_URL = os.getenv('ALBERT_URL', 'http://albert.visgean.me/api/')

API_CURRENT_PLAN_URL = urllib.parse.urljoin(API_URL, 'plans/latest/')
