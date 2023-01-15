
from rest_framework import serializers


class PaymentIntentCreateSerializer(serializers.Serializer):
    """
    Serializer to create payment intent.
    """
    amount = serializers.FloatField()


    class Meta:
        fields = ('amount',)
