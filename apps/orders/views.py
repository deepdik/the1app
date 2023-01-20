from asgiref.sync import async_to_sync
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.api_clients.platform import GeneralAPIClient
from apps.orders.models import APIMethodEnum, AvailableRecharge
from apps.orders.serializers import PlaceOrderSerializer, AvailableRechargeListSerializer
from apps.orders.utils.general_service import GeneralAPIService
from utils.exceptions import APIException400
from utils.response import response


# Create your views here.

class PlaceOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # GeneralAPIService().save_access_token()
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response(message="Order placed successfully")


class AvailableRechargeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        service_type = self.request.GET.get('service_type')
        if service_type:
            data = AvailableRecharge.objects.filter(
                is_active=True, service_type=service_type).values(
                "amount", "currency", "detail").order_by('amount')
            resp = {"data_recharge": data}
            return response(message="success", data=resp)
        raise APIException400({
            "error": "service_type is required"
        })
