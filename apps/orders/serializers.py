
from rest_framework import serializers


class PlaceOrderSerializer(serializers.Serializer):
    """
    Serializer to create order.
    """
    payment_intent_id = serializers.CharField()
    #order_id = serializers.CharField()


    class Meta:
        fields = ('payment_intent_id',)
