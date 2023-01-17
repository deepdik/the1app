from rest_framework import serializers

from utils.exceptions import APIException400, APIException500

SERVICE_CHOICES = (
    ("1", "DU_PREPAID"),
    ("2", "DU_POSTPAID"),
)

RECHARGE_TYPE = (
    ("1", "DATA"),
    ("2", "MINUTE")
)


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

    class Meta:
        fields = ('amount', 'service_type', 'recharge_number', 'recharge_type')
