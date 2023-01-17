from asgiref.sync import async_to_sync
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.api_clients.platform import GeneralAPIClient
from apps.orders.models import APIMethodEnum
from apps.orders.serializers import PlaceOrderSerializer
from apps.orders.utils.api_call_wrapper import async_api_caller
from apps.orders.utils.general_service import GeneralAPIService
from utils.response import response


# Create your views here.

class PlaceOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        #GeneralAPIService().save_access_token()
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response(message="Order placed successfully")
