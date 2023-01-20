import os

import environ

from the1backend.settings import BASE_DIR

env = environ.Env()
# reading .env file
if os.environ.get("ENV") == 'DEV':
    print("Started with DEV env")
    environ.Env.read_env(os.path.join(BASE_DIR, 'config/environ/dev.env'))
else:
    print("Started with local env")
    environ.Env.read_env(os.path.join(BASE_DIR, 'config/environ/local.env'))

"""
Token Generation API call :- https://qty.mbme.org:8080/v2/mbme/oauth/token
Balance & Payment API call :- https://qty.mbme.org:8080/v2/api/payment
Transaction Report URL :- https://qty.mbme.org:8080/v2/mbme/merchantTransactions
Check Status By Transaction Id :- https://qty.mbme.org:8080/v2/mbme/checkTransaction
Find All Pending Transaction :- https://qty.mbme.org:8080/v2/mbme/getPendingTransactions
Process Pending Payment :- https://qty.mbme.org:8080/v2/mbme/processTransaction
Merchant Balance check :- https://qty.mbme.org:8080/v2/mbme/merchantBalance
Transaction list: https://qty.mbme.org:8080/v2/mbme/merchantTransactions
"""

SITE_URL = env("SITE_URL")

ERROR_RETRY_COUNT = int(env('ERROR_RETRY_COUNT'))
HTTP_TOO_MANY_REQ_SLEEP = int(env('HTTP_TOO_MANY_REQ_SLEEP'))
HTTP_REQ_TIMEOUT_SLEEP = int(env('HTTP_REQ_TIMEOUT_SLEEP'))
ASYNC_TIMEOUT_SLEEP = int(env('ASYNC_TIMEOUT_SLEEP'))

MBME_PAY_USERNAME = env('MBME_PAY_USERNAME')
MBME_PAY_PASSWORD = env('MBME_PAY_PASSWORD')
MBME_BASE_URL = env('MBME_BASE_URL')
MBME_MERCHANT_ID = env('MBME_MERCHANT_ID')
MBME_AUTH_TOKEN = env("MBME_AUTH_TOKEN")
MBME_PAY_BAL= env("MBME_PAY_BAL")

DU_PREPAID_SERVICE_ID = env("DU_PREPAID_SERVICE_ID")
DU_PREPAID_MIN = env("DU_PREPAID_MIN")
DU_PREPAID_MAX = env("DU_PREPAID_MAX")

STRIP_PUBLISHABLE_KEY = env('STRIP_PUBLISHABLE_KEY')
STRIPE_CLIENT_SECRET = env('STRIPE_CLIENT_SECRET')
DEFAULT_CURRENCY = env('DEFAULT_CURRENCY')

