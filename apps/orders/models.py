from enum import Enum

from django.db import models
from rest_framework.authtoken.admin import User


# Create your models here.

class APIMethodEnum(str, Enum):
    POST = 'post'
    GET = 'get'
    DELETE = 'delete'
    PUT = 'put'
    PATCH = 'patch'


SERVICE_CHOICES = (
    ("1", "DU_PREPAID"),
    ("2", "DU_POSTPAID"),
)

RECHARGE_TYPE = (
    ("1", "DATA"),
    ("2", "MINUTE")
)

ORDER_SUB_STATUS = (
    ('1', 'PAYMENT_PROCESSING'),
    ('2', 'PAYMENT_COMPLETED'),
    ('3', 'PAYMENT_FAILED'),
    ('4', 'RECHARGE_PROCESSING'),
    ('5', 'RECHARGE_FAILED'),
    ('6', 'RECHARGE_COMPLETED')
)

ORDER_STATUS = (
    ('1', 'COMPLETED'),
    ('2', 'PROCESSING'),
    ('3', 'FAILED')
)


class AccessTokens(models.Model):
    access_token = models.TextField()
    valid_upto = models.DateTimeField()
    wallet_balance = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'access_tokens'

    def __str__(self):
        return str(self.id)


class MBMEVerifiedNumbers(models.Model):
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    recharge_type = models.CharField(max_length=100, choices=RECHARGE_TYPE)
    recharge_number = models.CharField(max_length=10)
    valid_upto = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mbme_verified_numbers'

    def __str__(self):
        return str(self.id)


class AvailableRecharge(models.Model):
    amount = models.FloatField()
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    recharge_type = models.CharField(max_length=100, choices=RECHARGE_TYPE)
    currency = models.CharField(max_length=20)
    detail = models.CharField(max_length=100)
    full_description = models.TextField(blank=True)
    validity = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'available_recharge'

    def __str__(self):
        return str(self.id)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    recharge_type = models.CharField(max_length=100, choices=RECHARGE_TYPE)
    recharge_number = models.CharField(max_length=10)
    amount = models.FloatField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS)
    sub_status = models.CharField(max_length=100, choices=ORDER_SUB_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return str(self.user.id) + '-' + str(self.id)


class MbmeOrderHistory(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='mbme_history')
    response = models.JSONField()
    transaction_id = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mbme_order_history'

    def __str__(self):
        return str(self.id)
