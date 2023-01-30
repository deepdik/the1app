"""
"""
from django.conf.urls import url
from django.urls import re_path, path

from rest_framework.routers import SimpleRouter

from apps.orders.views import PlaceOrderAPIView, AvailableRechargeAPIView, OrdersHistoryListAPIView, \
    CustomerBalanceAPIView, OrdersHistoryDetailAPIView, OrderViewSet, VerifyPrepaidAPIView

router = SimpleRouter()

router.register(r'', OrderViewSet, basename='order')


urlpatterns = [
    path('place', PlaceOrderAPIView.as_view(), name='order-place'),
    path('available/recharge', AvailableRechargeAPIView.as_view(), name='available-recharge'),
    path('history', OrdersHistoryListAPIView.as_view(), name='order-history'),
    path('history/detail', OrdersHistoryDetailAPIView.as_view(), name='order-history-detail'),
    path('postpaid/balance', CustomerBalanceAPIView.as_view(), name='postpaid-balance'),
    path('verify/prepaid', VerifyPrepaidAPIView.as_view(), name='verify-prepaid'),

    # Admin panel apis
    # path('', CustomerBalanceAPIView.as_view(), name='postpaid-balance'),
]

urlpatterns += router.urls
