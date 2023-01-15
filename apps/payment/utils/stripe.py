"""
"""
import stripe

from django.conf import settings
from django.urls import reverse

import logging

from apps.payment.utils.decorator import exception_handler

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Stripe(object):
    """
    Stripe
    """

    def __init__(self):
        self._configure()
        stripe.api_key = self.api_key

    def _configure(self):
        """ configure stripe keys """
        self.api_key = settings.STRIPE_CLIENT_SECRET

    @exception_handler
    def create_payment_intent(self, *args, **kwargs):
        """
        Method to create payment intent
        """
        amount = kwargs.get('amount', 0)
        currency = kwargs.get('currency', '')
        meta_data = {
            'order_id': kwargs.get('order_id', ''),
            'user_id': kwargs.get('user_id', ''),
            'amount': amount,
        }

        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency=currency,
            #payment_method_types=['card'],
            automatic_payment_methods={
                'enabled': True,
            },
            description="Payment for order",
            receipt_email=None,
            metadata=meta_data,
            #setup_future_usage='on_session',
            return_url=None,
        )
        payment_link = (settings.SITE_URL + reverse('stripe-payment')
                        + '?intent_id=' + intent['id'])

        return {"intent_id": payment_link}


    def retrive_payment_intent(self, *args, **kwargs):
        """
        """
        intent_id = kwargs.get('intent_id')
        intent = stripe.PaymentIntent.retrieve(
          intent_id,
        )
        return intent

    def get_or_create_customer(self, *args, **kwargs):
        """
        """
        name = kwargs.get('name')
        address = kwargs.get("address")
        email = kwargs.get("email")
        customer = stripe.Customer.create(
            address=address,
            email=email,
            name=name
        )
        return customer

    def cancel_payment_intent(self, *args, **kwargs):
        """
        To cancel payemnt intent
        """
        intent_id = kwargs.get('intent_id')
        intent = stripe.PaymentIntent.cancel(
            intent_id,
        )
        return intent
