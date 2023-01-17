from apps.orders.utils.general_service import GeneralAPIService


def refresh_access_token():
    GeneralAPIService().save_access_token()