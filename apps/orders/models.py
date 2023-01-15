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


class OrderDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_')
    credit_points = models.IntegerField(default=0)
    updated_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user.id) + '-' + str(self.id)