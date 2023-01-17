from django.conf import settings

from apps.orders.models import APIMethodEnum
from apps.orders.utils.api_call_wrapper import async_api_caller


class GeneralAPIClient:

    def __init__(self):
        self.base_url = settings.MBME_BASE_URL

    async def generate_token(self):
        payload = {
            "username": settings.MBME_PAY_USERNAME,
            "password": settings.MBME_PAY_PASSWORD
        }
        resp, status = await async_api_caller(
            url=settings.MBME_BASE_URL + settings.MBME_AUTH_TOKEN,
            method=APIMethodEnum.POST,
            data=payload
        )
        print(resp, status)
        if status:
            return resp, self.__get_response_status(resp)

    def __get_response_status(self, response):
        """
        120	TRANSACTIONID NOT FOUND FOR PREVIOUS REQUEST
        301	DUPLICATE TRANSACTIONID PROVIDED
        303	SERVICE NOT ENABLED FOR THE MERCHANT
        304	SERVICE NOT AVAILABLE.PLEASE CONTACT SUPPORT.
        305	MERCHANT NOT ENABLED
        888	INSUFFICIENT WALLET BALANCE
        901	REMOTE SERVER UNREACHABLE. TRY AGAIN LATER
        902	INVALID AUTHORIZATION
        991	PLEASE CONTACT MBME SUPPORT
        997	ERROR, PLEASE CONTACT MBME SUPPORT
        """
        if response.get("responseCode") == "000":
            return True
        else:
            return False
