from asgiref.sync import async_to_sync
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.api_clients.platform import GeneralAPIClient
from apps.orders.models import APIMethodEnum, AvailableRecharge, SERVICES_PROVIDER, MBME, Orders
from apps.orders.serializers import PlaceOrderSerializer, AvailableRechargeListSerializer, OrderListSerializer
from apps.orders.utils.general_service import GeneralAPIService
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


class OrdersHistoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        qs = Orders.objects.filter(user=request.user).order_by("created_at")
        data = OrderListSerializer(qs, many=True).data
        return response(message="success", data=data)


