from django.conf import settings

from apps.orders.models import APIMethodEnum
from apps.orders.utils.api_call_wrapper import async_api_caller


class GeneralAPIClient:

    def __init__(self):
        self.base_url = settings.MBME_BASE_URL

    def verify_customer_account(self):
        payload = {
            "username": settings.MBME_PAY_USERNAME,
            "password": settings.MBME_PAY_PASSWORD
        }
        resp, status = await async_api_caller(
            url=self.base_url + settings.MBME_AUTH_TOKEN,
            method=APIMethodEnum.POST,
            data=payload
        )