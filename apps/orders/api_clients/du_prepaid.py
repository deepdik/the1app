from asgiref.sync import async_to_sync
from django.conf import settings

from apps.orders.api_clients.platform import GeneralAPIClient
from apps.orders.models import APIMethodEnum
from apps.orders.utils.api_call_wrapper import sync_api_caller
from apps.orders.utils.utils import get_transaction_id
from utils.exceptions import APIException500, APIException503


class DUPrepaidAPIClient:

    def __init__(self):
        self.base_url = settings.MBME_BASE_URL


    def verify_customer_account(self, number):
        """Use API Method balance to verify the consumer's account using the unique
            transaction Id."""
        payload = {
            "transactionId": get_transaction_id(),
            "merchantId": settings.MBME_MERCHANT_ID,
            "serviceId": settings.DU_PREPAID_SERVICE_ID,
            "method": "balance",
            "reqField1": number
        }
        token = GeneralAPIClient().get_access_token()
        if not token:
            raise APIException503()

        headers = {"Authorization": token}
        resp, status = sync_api_caller(
            url=self.base_url + settings.MBME_PAY_BAL,
            method=APIMethodEnum.POST,
            data=payload,
            headers=headers,
            retry=1
        )
        if not status:
            raise APIException503()

        return self.__get_response_message(resp)
    def __get_response_message(self, response):
        if response.get("responseCode") == "000":
            return True, "Number verified successfully"
        elif response.get("responseCode") in ("302", "905", "906", "907"):
            return False, "Invalid Mobile Number"
        else:
            raise APIException503()
