"""
"""
from django.conf.urls import url
from django.urls import re_path, path

from rest_framework.routers import SimpleRouter

from apps.orders.views import PlaceOrderAPIView, AvailableRechargeAPIView, OrdersHistoryListAPIView, \
    CustomerBalanceAPIView, OrdersHistoryDetailAPIView

router = SimpleRouter()

urlpatterns = [
    path('place', PlaceOrderAPIView.as_view(), name='order-place'),
    path('available/recharge', AvailableRechargeAPIView.as_view(), name='available-recharge'),
    path('history', OrdersHistoryListAPIView.as_view(), name='order-history'),
    path('history/detail', OrdersHistoryDetailAPIView.as_view(), name='order-history-detail'),
    path('postpaid/balance', CustomerBalanceAPIView.as_view(), name='postpaid-balance'),
]

urlpatterns += router.urls
