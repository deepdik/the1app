import asyncio
import datetime

from asgiref.sync import sync_to_async, async_to_sync
from django.conf import settings
from rest_framework import serializers

from apps.orders.api_clients.du_prepaid import DUPrepaidAPIClient
from apps.orders.models import SERVICE_CHOICES, RECHARGE_TYPE, AvailableRecharge, VerifiedNumbers, SERVICES_PROVIDER, \
    MBME, DU_PREPAID, MINUTE, DATA
from utils.exceptions import APIException400, APIException500


class PaymentIntentCreateSerializer(serializers.Serializer):
    """
    Serializer to create payment intent.
    """
    amount = serializers.FloatField()
    service_type = serializers.ChoiceField(choices=SERVICE_CHOICES)
    recharge_number = serializers.CharField(max_length=10)
    recharge_type = serializers.ChoiceField(choices=RECHARGE_TYPE)

    def validate_recharge_number(self, value):
        if not value.isdigit():
            raise APIException400({
                "error": "Recharge Number is not valid"
            })
        return value

    def validate_amount(self, value):
        # validate price range
        return value

    def validate(self, attrs):
        service_type = attrs["service_type"]
        recharge_type = attrs["recharge_type"]
        amount = attrs["amount"]
        recharge_number = attrs["recharge_number"]
        # for DU prepaid
        if service_type == DU_PREPAID:
            if recharge_type == MINUTE and (
                    amount < int(settings.DU_PREPAID_MIN) or amount > int(settings.DU_PREPAID_MAX)):
                raise APIException400({
                    "error": f"Recharge amount should be between {settings.DU_PREPAID_MIN}-{settings.DU_PREPAID_MAX}"
                })
            elif recharge_type == DATA:
                # for data recharge
                qs = AvailableRecharge.objects.filter(
                    service_type=service_type,
                    recharge_type=recharge_type,
                    amount=amount,
                    is_active=True,
                    service_provider=MBME,
                    currency=settings.DEFAULT_CURRENCY
                )
                if not qs.exists():
                    raise APIException400({
                        "error": "Data recharge amount is invalid"
                    })
            # verify number
            # check first in DB
            qs = VerifiedNumbers.objects.filter(
                service_type=service_type,
                recharge_type=recharge_type,
                recharge_number=recharge_number,
                service_provider=MBME,
                valid_upto__gt=datetime.datetime.now()
            )
            if not qs.exists():
                status, message = DUPrepaidAPIClient().verify_customer_account(recharge_number)
                # save in DB
                VerifiedNumbers.objects.update_or_create(
                    service_type=service_type,
                    recharge_number=recharge_number,
                    service_provider=MBME,
                    defaults={"valid_upto": datetime.datetime.now() + datetime.timedelta(days=1),
                              "recharge_type": recharge_type}
                )
                if not status:
                    raise APIException400({
                        "error": message
                    })

        return attrs

    class Meta:
        fields = ('amount', 'service_type', 'recharge_number', 'recharge_type')
