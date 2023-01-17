from django.contrib import admin

from apps.orders.models import AccessTokens


# Register your models here.


@admin.register(AccessTokens)
class AccessTokensAdmin(admin.ModelAdmin):
    list_display = ('id', 'valid_upto', "updated_at", )