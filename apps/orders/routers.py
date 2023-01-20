"""
"""
from django.conf.urls import url
from django.urls import re_path, path

from rest_framework.routers import SimpleRouter

from apps.orders.views import PlaceOrderAPIView, AvailableRechargeAPIView

router = SimpleRouter()

urlpatterns = [
    path('place', PlaceOrderAPIView.as_view(), name='order-place'),
    path('available/recharge', AvailableRechargeAPIView.as_view(), name='available-recharge'),

]

urlpatterns += router.urls
