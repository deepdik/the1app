from rest_framework import serializers

from apps.orders.models import AvailableRecharge
from utils.exceptions import APIException400


class PlaceOrderSerializer(serializers.Serializer):
    """
    Serializer to create order.
    """
    payment_intent_id = serializers.CharField()

    # order_id = serializers.CharField()

    class Meta:
        fields = ('payment_intent_id',)


class AvailableRechargeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableRecharge
        fields = "__all__"


