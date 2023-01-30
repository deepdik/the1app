from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.orders.api_clients.du_postpaid import DUPostpaidAPIClient
from apps.orders.api_clients.du_prepaid import DUPrepaidAPIClient
from apps.orders.models import AvailableRecharge, MBME, Orders
from apps.orders.serializers import PlaceOrderSerializer, OrderDetailSerializer, \
    OrderDetailViewSerializer, OrderListViewSerializer
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
            if not number.isdigit() or len(number) > 10:
                raise APIException400({
                    "error": "Invalid mobile Number"
                })
            data = DUPostpaidAPIClient().get_customer_balance(number)
            return response(message="success", data=data)
        raise APIException400({
            "error": "number is required"
        })


class VerifyPrepaidAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        number = self.request.GET.get('number')
        if number:
            if not number.isdigit() or len(number) > 10:
                raise APIException400({
                    "error": "Invalid mobile Number"
                })
            status, msg = DUPrepaidAPIClient().verify_customer_account(number)
            if not status:
                raise APIException400({
                    "error": msg
                })
            return response(message=msg)
        raise APIException400({
            "error": "number is required"
        })


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderListViewSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('created_at',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailViewSerializer
        return super(OrderViewSet, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        response_data = OrderHistory(request).get_order_list_for_admin()
        return response(data=response_data, message="success")

    def retrieve(self, request, *args, **kwargs):
        response_data = super(OrderViewSet, self).retrieve(request, *args, **kwargs).data
        return response(data=response_data, message="success")
