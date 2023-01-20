import datetime

from django.conf import settings
from django.utils import timezone

from apps.orders.models import APIMethodEnum, AccessTokens
from apps.orders.utils.api_call_wrapper import sync_api_caller


class GeneralAPIClient:

    def __init__(self):
        self.base_url = settings.MBME_BASE_URL

    def __generate_token(self):
        payload = {
            "username": settings.MBME_PAY_USERNAME,
            "password": settings.MBME_PAY_PASSWORD
        }
        resp, status = sync_api_caller(
            url=settings.MBME_BASE_URL + settings.MBME_AUTH_TOKEN,
            method=APIMethodEnum.POST,
            data=payload,
            retry=1
        )
        print(resp, status)
        if status:
            resp_status = self.__get_response_status(resp)
            if resp_status:
                valid_upto = datetime.datetime.now() + datetime.timedelta(minutes=4, seconds=50)
                AccessTokens.objects.create(
                    access_token=resp["accessToken"],
                    valid_upto=valid_upto,
                    wallet_balance=resp["walletBalance"]
                )
                return resp["accessToken"]
            return None
        return None

    def get_access_token(self):
        print("Trying to get access token")
        qs = AccessTokens.objects.filter(valid_upto__gt=datetime.datetime.now())
        if qs.exists():
            return qs[0].access_token
        else:
            return self.__generate_token()

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
        elif response.get("responseCode") in ("120", "301", "304"):
            return False
        else:
            return False

    def get_all_transaction_report(self, from_date, to_date):
        pass
