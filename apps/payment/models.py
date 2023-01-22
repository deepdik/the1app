from django.db import models
from django.contrib.auth.models import User

from apps.orders.models import Orders

TRANSACTION_PROCESSING, TRANSACTION_FAILED, TRANSACTION_COMPLETED, TRANSACTION_CANCELLED = "1", "2", "3", "4"
TRANSACTION_STATUS = (
    (TRANSACTION_PROCESSING, "PROCESSING"),
    (TRANSACTION_FAILED, "FAILED"),
    (TRANSACTION_COMPLETED, "COMPLETED"),
    (TRANSACTION_CANCELLED, "CANCELLED")
)


class StripeCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stripe_customer')
    customer_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class StripeTransactions(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payment')
    payment_intent = models.CharField(max_length=500)
    gateway_response = models.TextField()
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserCreditPoint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_points')
    credit_points = models.IntegerField(default=0)
    updated_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user.id) + '-' + str(self.id)


class CreditPointTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    transaction_id = models.AutoField(primary_key=True, unique=True)
    reason_title = models.CharField(max_length=100, default='')
    reason_desc = models.TextField(null=True, blank=True)
    order_id = models.CharField(max_length=10, null=True, blank=True, default=None)
    referral_id = models.CharField(null=True, blank=True, default=None, max_length=10)
    debited_points = models.IntegerField(default=0)
    credited_points = models.IntegerField(default=0)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.transaction_id)




