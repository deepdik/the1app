"""
"""
import datetime
import json
import MySQLdb
import stripe

from django.conf import settings


class StripeWebhook:
    """
    """
    stripe.api_key = settings.STRIPE_CLIENT_SECRET

    EVENT_TYPES = (
        'account.updated',
        'payment_intent.succeeded',
        'payment_intent.payment_failed'
    )
    # payment for types
    INVOICE, SUBSCRIPTION = 1, 2

    def get_event(self, data):
        """
        get required event
        """
        event = data['type']
        if event in self.EVENT_TYPES:
            return event
        return None

    def get_values_string(self, value):
        if value:
            return "{0}".format(value)
        else:
            return "NULL"

    def connect_payment_update_hook(self, data):
        """
        """
        try:
            self.connect_db()
            if self.cursor:
                object_data = data['data']['object']
                # log incomming data
                pylogging.logger_info(str(object_data))
                if object_data['status'] == 'succeeded':
                    self._save_inv_payment_detail(
                        data=object_data
                    )
                self._create_transaction_detail(
                    data=object_data
                )
        except Exception as e:
            pylogging.logger_info("Webhook Error:: <event_type::payment_intent> :: "
                                  + str(e)
                                  )
        pylogging.logger_info("Webhook Success <event_type::{}>".format(
            data['type']))
        self.db_connection.close()


    def _create_transaction_detail(self, *args, **kwargs):
        """
        To save transactions details
        """
        data = kwargs.get('data', {})
        if data:
            insert_query = """INSERT into transaction_detail
                (entity, entity_id, gatway_used, gateway_response, status,
                created_at, updated_at, user_id) values (
                %s, %s, %s, %s, %s, %s, %s, %s)"""

            created_at = datetime.datetime.now()
            entity_id = data['metadata'].get('invoice_id')
            user_id = data['metadata'].get('user_id')
            gatway_used = self.get_payment_gatway('stripe')
            if data['status'] == 'succeeded':
                # success
                status = 1
            else:
                status = 2

            values = (
                self.get_values_string(self.INVOICE),
                self.get_values_string(entity_id),
                self.get_values_string(gatway_used),
                json.dumps(data),
                self.get_values_string(status),
                self.get_values_string(created_at),
                self.get_values_string(created_at),
                self.get_values_string(user_id),
            )
            self.cursor.execute(insert_query, values)
            self.db_connection.commit()
