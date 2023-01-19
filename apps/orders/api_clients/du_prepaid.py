from django.conf import settings

from apps.orders.models import APIMethodEnum
from apps.orders.utils.api_call_wrapper import async_api_caller


class GeneralAPIClient:

    def __init__(self):
        self.base_url = settings.MBME_BASE_URL

    def verify_customer_account(self):
        """Use API Method balance to verify the consumer's account using the unique
            transaction Id."""
        payload = {
                "transactionId": "191217984****89166",
                "merchantId": settings.MBME_MERCHANT_ID,
                "merchantLocation": "FEWA RAK HQ",
                "serviceId": "1",
                "method": "balance",
                "lang": "en",
                "reqField1": "0559035788"
            }
        resp, status = await async_api_caller(
            url=self.base_url + settings.MBME_AUTH_TOKEN,
            method=APIMethodEnum.POST,
            data=payload
        )

