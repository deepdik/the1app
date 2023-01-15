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

    def connect_db(self):
        """
        Making connection with the TrueRev DB
        """
        self.db_connection = MySQLdb.connect(
            user=settings.USERNAME,
            password=settings.PASSWORD,
            host=settings.HOST,
            db=settings.DB_NAME,
        )
        self.cursor = self.db_connection.cursor()

    def close_db_connection(self):
        """
        close connection of Database
        """
        self.db_connection.close()

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

    def connect_account_update_hook(self, data):
        """
        Webhook called whenever account is updated.
        """
        try:
            self.connect_db()
            if self.cursor:
                object_data = data['data']['object']
                pylogging.logger_info(str(object_data))
                self._save_conn_account_info(object_data)
        except Exception as e:
            pylogging.logger_info("Webhook Error:: <event_type::connect account> :: "
                                  + str(e)
                                  )

        pylogging.logger_info(
            "Webhook Success <event_type::{0} for user_id: {1}".format(
                data['type'],
                object_data['metadata'].get('user_id')))
        self.db_connection.close()

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

    def get_payment_gatway(self, name):
        """
        get list of gateway
        """
        query = """select id from master_payment_gateway where name=%s"""
        self.cursor.execute(
            query, (name,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def _check_create_or_update_account(self, data, gatway_used, user_id):
        """
        """
        query = """select * from user_payment_details where user_id=%s and gatway_used=%s"""
        self.cursor.execute(
            query, (user_id, gatway_used,)
        )
        results = self.cursor.fetchall()
        acc_id = data['id']
        for result in results:
            res = json.loads(result[3])
            if acc_id == res['id']:
                return result

        return None

    def retrive_connect_account(self, user_id, gatway_used):
        """
        retrive user account detail
        """
        self.connect_db()
        gatway_used = self.get_payment_gatway(gatway_used)
        query = """select * from user_payment_details where user_id=%s
             and gatway_used=%s"""
        self.cursor.execute(
            query, (user_id, gatway_used,)
        )
        results = self.cursor.fetchall()
        self.close_db_connection()
        if results:
            res = json.loads(results[0][3])
            return {'id': res['id'],
                    'status': res['details_submitted'],
                    }
        return None

    def retrive_invoice_detail(self, inv_id):
        """
        retrive invoice detail
        """
        self.connect_db()
        query = """select * from invoice_payment where invoice_id=%s"""
        self.cursor.execute(
            query, (inv_id,)
        )
        results = self.cursor.fetchall()
        self.close_db_connection()
        if results:
            return results
        return None

    def _update_conn_account(self, data, obj_id):
        """
        """
        query = """Update user_payment_details set payment_gateway_info=%s,
         updated_at=%s where id=%s"""

        updated_at = datetime.datetime.now()
        values = (
            json.dumps(data),
            self.get_values_string(updated_at),
            self.get_values_string(obj_id),
        )
        self.cursor.execute(query, values)
        self.db_connection.commit()

    def _save_conn_account_info(self, data):
        """
        """
        if data:
            gatway_used = self.get_payment_gatway('stripe')
            user_id = data['metadata'].get('user_id')

            obj = self._check_create_or_update_account(
                data, gatway_used, user_id)

            # if account exists then update else create new one
            if obj:
                self._update_conn_account(data, obj[0])
            else:
                insert_query = """INSERT into user_payment_details
                    (user_id, gatway_used, payment_gateway_info, is_deault,
                    status, created_at, updated_at) values (%s, %s, %s, %s, %s,
                     %s, %s)"""
                # 1-connected, 2-disconnected, 3- deleted
                status = 1
                is_deault = 0
                created_at = datetime.datetime.now()
                values = (
                    self.get_values_string(user_id),
                    self.get_values_string(gatway_used),
                    json.dumps(data),
                    self.get_values_string(is_deault),
                    self.get_values_string(status),
                    self.get_values_string(created_at),
                    self.get_values_string(created_at)

                )
                self.cursor.execute(insert_query, values)
                self.db_connection.commit()

    def _save_inv_payment_detail(self, *args, **kwargs):
        """
        """
        data = kwargs.get('data', None)
        if data:
            query = """INSERT into invoice_payment
                (invoice_id, company_id, amount, integration_origin_id,
                status, paid_at, remaining_amount) values (
                %s, %s, %s, %s, %s, %s, %s)"""
            paid_at = datetime.datetime.now()
            invoice_id = data['metadata'].get('invoice_id')
            status = 1
            integration_origin_id = data['metadata'].get('integration_origin_id')
            amount = data['metadata'].get('amount')
            company_id = data['metadata'].get('company_id')
            remaining_amount = 0
            values = (
                self.get_values_string(invoice_id),
                self.get_values_string(company_id),
                self.get_values_string(amount),
                self.get_values_string(integration_origin_id),
                self.get_values_string(status),
                self.get_values_string(paid_at),
                self.get_values_string(remaining_amount),
            )
            self.cursor.execute(query, values)
            self.db_connection.commit()

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
