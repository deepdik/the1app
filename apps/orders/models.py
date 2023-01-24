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


MBME = "1"
SERVICES_PROVIDER = (
    (MBME, "MBME"),
)

DU_PREPAID, DU_POSTPAID = "1", "2"
SERVICE_CHOICES = (
    (DU_PREPAID, "DU_PREPAID"),
    (DU_POSTPAID, "DU_POSTPAID"),
)

DATA, MINUTE = "1", "2"
RECHARGE_TYPE = (
    (DATA, "DATA"),
    (MINUTE, "MINUTE")
)

PAYMENT_PROCESSING, PAYMENT_COMPLETED, PAYMENT_FAILED = "1", "2", "3"
RECHARGE_PROCESSING, RECHARGE_FAILED, RECHARGE_COMPLETED = "4", "5", "6"
ORDER_SUB_STATUS = (
    (PAYMENT_PROCESSING, 'PAYMENT_PROCESSING'),
    (PAYMENT_COMPLETED, 'PAYMENT_COMPLETED'),
    (PAYMENT_FAILED, 'PAYMENT_FAILED'),
    (RECHARGE_PROCESSING, 'RECHARGE_PROCESSING'),
    (RECHARGE_FAILED, 'RECHARGE_FAILED'),
    (RECHARGE_COMPLETED, 'RECHARGE_COMPLETED')
)

COMPLETED, PROCESSING, FAILED = "1", "2", "3"
ORDER_STATUS = (
    (COMPLETED, 'COMPLETED'),
    (PROCESSING, 'PROCESSING'),
    (FAILED, 'FAILED')
)


class AccessTokens(models.Model):
    access_token = models.TextField()
    service_provider = models.CharField(max_length=100, choices=SERVICES_PROVIDER)
    valid_upto = models.DateTimeField()
    wallet_balance = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'access_tokens'

    def __str__(self):
        return str(self.id)


class VerifiedNumbers(models.Model):
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    recharge_type = models.CharField(max_length=100, choices=RECHARGE_TYPE)
    service_provider = models.CharField(max_length=100, choices=SERVICES_PROVIDER)
    recharge_number = models.CharField(max_length=10)
    valid_upto = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'verified_numbers'

    def __str__(self):
        return str(self.id)


class PostpaidAccountBalance(models.Model):
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    recharge_type = models.CharField(max_length=100, choices=RECHARGE_TYPE, blank=True, null=True)
    service_provider = models.CharField(max_length=100, choices=SERVICES_PROVIDER)
    recharge_number = models.CharField(max_length=10)
    balance = models.CharField(max_length=10)
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    response = models.JSONField(blank=True, null=True)
    valid_upto = models.DateTimeField()
    recharge_transaction_id = models.CharField(max_length=500, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'postpaid_account_balance'

    def __str__(self):
        return str(self.id)


class AvailableRecharge(models.Model):
    amount = models.FloatField()
    service_provider = models.CharField(max_length=100, choices=SERVICES_PROVIDER)
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
    service_provider = models.CharField(max_length=100, choices=SERVICES_PROVIDER)
    recharge_number = models.CharField(max_length=10)
    amount = models.FloatField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS)
    sub_status = models.CharField(max_length=100, choices=ORDER_SUB_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return str(self.user.id) + '-' + str(self.id)


class OrdersDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_detail')
    retry_count = models.IntegerField()
    last_response = models.JSONField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # pending_reason = models.CharField(max_length=100, choices=)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders_details'

    def __str__(self):
        return str(self.id)
