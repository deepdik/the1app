"""
"""
from django.conf.urls import url
from django.urls import re_path, path

from rest_framework.routers import SimpleRouter

from apps.payment.views import StripePaymentAPIView, StripeWebhookAPIView, StripePaymentView

router = SimpleRouter()

urlpatterns = [
    path('stripe/initiate', StripePaymentAPIView.as_view(), name='stripe-initiate-payment'),
    path('stripe/webhook', StripeWebhookAPIView.as_view(), name='stripe-webhook'),
    path('stripe/payment', StripePaymentView.as_view(), name='stripe-payment'),

]

urlpatterns += router.urls
