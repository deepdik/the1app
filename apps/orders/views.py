from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.orders.api_clients.du_postpaid import DUPostpaidAPIClient
from apps.orders.models import AvailableRecharge, MBME, Orders
from apps.orders.serializers import PlaceOrderSerializer, OrderListSerializer
from apps.orders.utils.order_history_service import OrderHistory
from apps.orders.utils.order_place_service import OrderService
from utils.exceptions import APIException400
from utils.response import response


# Create your views here.

class PlaceOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status, msg = OrderService(request.data.get("payment_intent_id"), request).place_order()
        return response(data={"status": status}, message=msg)


class AvailableRechargeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        service_type = self.request.GET.get('service_type')
        service_provide = MBME
        if service_type:
            data = AvailableRecharge.objects.filter(
                is_active=True, service_type=service_type, service_provider=service_provide).values(
                "amount", "currency", "detail", "validity", "full_description").order_by('amount')
            resp = {"data_recharge": data}
            return response(message="success", data=resp)
        raise APIException400({
            "error": "service_type is required"
        })


class OrdersHistoryListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = OrderHistory(request).get_order_list()
        return response(message="success", data=data)


class OrdersHistoryDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if not self.request.GET.get('order_id'):
            raise APIException400({
                "error": "order_id is required"
            })
        data = OrderHistory(request).get_order_detail()
        return response(message="success", data=data)


class CustomerBalanceAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        number = self.request.GET.get('number')
        if number:
            data = DUPostpaidAPIClient().get_customer_balance(number)
            return response(message="success", data=data)
        raise APIException400({
            "error": "number is required"
        })