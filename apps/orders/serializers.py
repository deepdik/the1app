from rest_framework import serializers

from apps.orders.models import AvailableRecharge, Orders, PostpaidAccountBalance


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
        fields = ("created_at", "status", "amount",
                  "service_type", "order_id")


class OrderDetailSerializer(serializers.ModelSerializer):
    transaction_details = serializers.SerializerMethodField()

    def get_transaction_details(self, obj):
        payment_obj = obj.payment.first()
        if payment_obj:
            return {"transaction_id": payment_obj.transaction_id,
                    "payment_method": payment_obj.payment_method, "payment_provider": payment_obj.payment_provider}
        return None

    class Meta:
        model = Orders
        fields = ("created_at", "status", "amount", "recharge_number",
                  "service_type", "recharge_type", "transaction_details", "order_id")


class PostpaidAccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostpaidAccountBalance
        fields = ("customer_name", "balance", "recharge_number", "recharge_transaction_id")
