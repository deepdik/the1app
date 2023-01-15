from django.conf.urls import include, url


urlpatterns = [
   	url("payment/", include('apps.payment.routers')),
    url("orders/", include('apps.orders.routers')),
]
