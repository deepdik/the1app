import asyncio
import datetime

from asgiref.sync import sync_to_async, async_to_sync
from django.conf import settings
from rest_framework import serializers
from stripe.api_resources.payment_method import PaymentMethod

from apps.orders.api_clients.du_prepaid import DUPrepaidAPIClient
from apps.orders.models import SERVICE_CHOICES, RECHARGE_TYPE, AvailableRecharge, VerifiedNumbers, SERVICES_PROVIDER, \
    MBME, DU_PREPAID, MINUTE, DATA, Orders, DU_POSTPAID
from apps.payment.models import PaymentTransactions, PaymentMethods
from utils.exceptions import APIException400, APIException500


class PaymentIntentCreateSerializer(serializers.Serializer):
    """
    Serializer to create payment intent.
    """
    amount = serializers.FloatField()
    service_type = serializers.ChoiceField(choices=SERVICE_CHOICES)
    recharge_number = serializers.CharField(max_length=10)
    recharge_type = serializers.ChoiceField(choices=RECHARGE_TYPE, allow_blank=True, allow_null=True)
    recharge_transaction_id = serializers.CharField(allow_blank=True, allow_null=True)

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
        # DU postpaid
        if service_type == DU_POSTPAID and not attrs.get("recharge_transaction_id"):
            raise APIException400({
                "error": f"recharge_transaction_id is required for DU Postpaid"
            })

        # for DU prepaid
        if service_type == DU_PREPAID:
            if not recharge_type:
                raise APIException400({
                    "error": f"recharge_type is required for DU Prepaid"
                })

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


class UserPaymentHistoryListSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_order_id(self, obj):
        return obj.order.order_id

    def get_amount(self, obj):
        return obj.order.amount

    def get_user_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    class Meta:
        model = PaymentTransactions
        fields = ("transaction_id", "created_at", "payment_provider",
                  "payment_method", "status", "amount", "order_id", "user", "user_name")


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethods
        fields = "__all__"
        read_only_fields = ("state", "id")


class PaymentMethodListSerializer(serializers.ModelSerializer):
    active_methods = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    def get_country_name(self, obj):
        return obj.country.name

    def get_active_methods(self, obj):
        count = 0
        count += 1 if obj.debit_card else 0
        count += 1 if obj.credit_card else 0
        count += 1 if obj.credit_points else 0
        count += 1 if obj.apple_pay else 0
        return count

    def get_city_name(self, obj):
        return obj.city.name

    class Meta:
        model = PaymentMethods
        fields = ("id", "active_methods", "country_name", "city_name", "provider")
