import datetime

from enum import Enum

from django.utils import timezone

from apps.orders.models import Orders, DU_PREPAID, DU_POSTPAID
from apps.orders.serializers import OrderListSerializer, OrderDetailSerializer
from utils.exceptions import APIException400, APIException404


class MonthFilter(Enum):
    TODAY = "1"
    THIS_WEEK = "2"
    THIS_MONTH = "3"
    THIS_YEAR = "4"
    ANY = "5"


class OrderHistoryCategory(Enum):
    PREPAID = "1"
    POSTPAID = "2"


class ORDER_TYPE(Enum):
    MOBILE = "1"
    TRANSPORT = "2"
    ANY = "3"


class OrderHistory:

    def __init__(self, request):
        self.request = request

    def get_order_list(self):
        """1-mobile recharge, 2-transport recharge, 3-all"""
        limit = int(self.request.GET.get('limit', 10))
        offset = int(self.request.GET.get('offset', 0))
        data = {"limit": limit, "offset": offset}
        if not self.request.GET.get('order_type'):
            raise APIException400({
                "error": "order_type is required"
            })
        qs = Orders.objects.filter()

        if self.request.GET.get('order_type') in (ORDER_TYPE.MOBILE.value, ORDER_TYPE.ANY.value):

            if self.request.GET.get('search_by'):
                print(self.request.GET.get('search_by'))
                qs = qs.filter(order_id=self.request.GET.get('search_by'))

            in_filter = []
            if self.request.GET.get('category') == OrderHistoryCategory.PREPAID.value:
                in_filter.append(DU_PREPAID)
            elif self.request.GET.get('category') == OrderHistoryCategory.POSTPAID.value:
                in_filter.append(DU_POSTPAID)
            else:
                in_filter = [DU_PREPAID, DU_POSTPAID]

            qs = qs.filter(
                service_type__in=in_filter
            ).order_by("-created_at")

            if self.request.GET.get('month') == MonthFilter.TODAY.value:
                qs = qs.filter(created_at__date=timezone.now().today())
            elif self.request.GET.get('month') == MonthFilter.THIS_WEEK.value:
                qs = qs.filter(created_at__week=timezone.now().isocalendar()[1])
            elif self.request.GET.get('month') == MonthFilter.THIS_MONTH.value:
                qs = qs.filter(created_at__month=timezone.now().now().month)
            elif self.request.GET.get('month') == MonthFilter.THIS_YEAR.value:
                qs = qs.filter(created_at__year=timezone.now().now().year)

            # data["total"] = qs.count()
            qs = qs[offset:limit + offset]
            data["mobile_recharge"] = OrderListSerializer(qs, many=True).data

        if self.request.GET.get('order_type') in (ORDER_TYPE.TRANSPORT.value, ORDER_TYPE.ANY.value):
            data["transport_recharge"] = []

        return data

    def get_order_detail(self):
        qs = Orders.objects.filter(user=self.request.user,
                                   order_id=self.request.GET.get('order_id'))
        if not qs.exists():
            raise APIException404({
                "error": "no resource found"
            })
        data = OrderDetailSerializer(qs, many=True).data
        return data
