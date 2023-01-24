from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(UserCreditPoint)
admin.site.register(CreditPointTransaction)
admin.site.register(PaymentTransactions)
admin.site.register(StripeCustomer)


