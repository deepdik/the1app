import os

import environ

from the1backend.settings import BASE_DIR

env = environ.Env()
# reading .env file
if os.environ.get("ENV") == 'DEV':
    environ.Env.read_env(os.path.join(BASE_DIR, 'config/environ/dev.env'))
else:
    environ.Env.read_env(os.path.join(BASE_DIR, 'config/environ/local.env'))

ERROR_RETRY_COUNT = env('ERROR_RETRY_COUNT')
STRIPE_CLIENT_SECRET = env('STRIPE_CLIENT_SECRET')
MBME_PAY_USERNAME = env('MBME_PAY_USERNAME')
MBME_PAY_PASSWORD = env('MBME_PAY_PASSWORD')
MBME_BASE_URL = env('MBME_BASE_URL')
MBME_MERCHANT_ID = env('MBME_MERCHANT_ID')
STRIP_PUBLISHABLE_KEY = env('STRIP_PUBLISHABLE_KEY')
STRIPE_CLIENT_SECRET = env('STRIPE_CLIENT_SECRET')
DEFAULT_CURRENCY = env('DEFAULT_CURRENCY')
SITE_URL = env("SITE_URL")
