from apps.orders.models import Orders, DU_PREPAID, DU_POSTPAID
from apps.orders.serializers import OrderListSerializer, OrderDetailSerializer
from utils.exceptions import APIException400, APIException404


class OrderHistory:

    def __init__(self, request):
        self.request = request

    def get_order_list(self):
        """1-mobile recharge, 2-transport recharge, 3-all"""
        if not self.request.GET.get('order_type'):
            raise APIException400({
                "error": "order_type is required"
            })
        data = {}
        if self.request.GET.get('order_type') in ("1", "3"):
            qs = Orders.objects.filter(
                user=self.request.user,
                service_type__in=[DU_PREPAID, DU_POSTPAID]
            ).order_by("-created_at")
            data["mobile_recharge"] = OrderListSerializer(qs, many=True).data

        return data

    def get_order_detail(self):
        qs = Orders.objects.filter(user=self.request.user,
                                   id=self.request.GET.get('order_id'))
        if not qs.exists():
            raise APIException404({
                "error": "no resource found"
            })
        data = OrderDetailSerializer(qs, many=True).data
        return data
