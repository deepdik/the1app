from asgiref.sync import async_to_sync
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import APIMethodEnum
from apps.orders.utils.api_call_wrapper import async_api_caller


# Create your views here.

class PlaceOrderAPIView(APIView):

    @async_to_sync
    async def post(self, request, *args, **kwargs):
        # await async_api_caller("", APIMethodEnum.GET)
        return Response("", 200)
