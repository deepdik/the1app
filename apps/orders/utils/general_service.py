import logging
from datetime import datetime, timedelta, timezone, date
import asyncio
from apps.orders.api_clients.platform import GeneralAPIClient
from apps.orders.models import AccessTokens

logger = logging.getLogger(__name__)


class GeneralAPIService:

    def save_access_token(self):
        resp, status = asyncio.run(GeneralAPIClient().generate_token())
        logger.debug(resp)
        if status:
            valid_upto = datetime.now(tz=timezone.utc) + timedelta(minutes=4, seconds=50)
            AccessTokens.objects.create(
                access_token=resp["accessToken"],
                valid_upto=valid_upto,
                wallet_balance=resp["walletBalance"]
            )

    def get_all_pending_transactions(self, from_date: date, to_date: date):
        pass

    def process_pending_transactions(self):
        pass

    def get_transaction_status(self, transaction_id):
        pass

    def get_transactions_report(self, transactions):
        pass
