"""
"""
from django.conf.urls import url
from django.urls import re_path, path

from rest_framework.routers import SimpleRouter

from apps.orders.views import TestAPIView

router = SimpleRouter()

urlpatterns = [
    path('place', TestAPIView.as_view(), name='stripe-webhook'),
]

urlpatterns += router.urls
