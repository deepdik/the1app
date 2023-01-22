from rest_framework import serializers

from apps.orders.models import AvailableRecharge, Orders


class PlaceOrderSerializer(serializers.Serializer):
    """
    Serializer to create order.
    """
    payment_intent_id = serializers.CharField()

    class Meta:
        fields = ('payment_intent_id',)


class AvailableRechargeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableRecharge
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ("created_at", "status", "amount", "recharge_number",
                  "service_type", "recharge_type")