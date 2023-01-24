from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import SERVICES_PROVIDER, Orders
from apps.payment.serializers import PaymentIntentCreateSerializer
from apps.payment.utils.stripe import Stripe
from apps.payment.utils.webhooks import StripeWebhook
from utils.response import response


class StripePaymentView(View):
    """
    View to create payment link
    """

    def get(self, request, *args, **kwargs):
        """
        """
        stripe_obj = Stripe()
        intent_id = request.GET.get('intent_id')
        context = {}
        if intent_id:
            # check payment intent
            stripe_obj = Stripe()
            response = stripe_obj.retrive_payment_intent(
                intent_id=intent_id
            )
            # if invoice is already paid then cancel the intent
            # if response.get('status') != 'canceled':
            #     response = stripe_obj.cancel_payment_intent(
            #         intent_id=intent_id)

            print(response)
            if response["data"].get('status') in ("requires_payment_method", "requires_source"):
                secret_id = response["data"]['client_secret']
                amount = response["data"]['metadata']['amount']
            else:
                print(response)
                return render(request, 'expire.html', context)

            context = {
                'client_secret': secret_id,
                'stripe_pub_key': settings.STRIP_PUBLISHABLE_KEY,
                'amount': amount,
                'success_url': ""
            }
            return render(request, 'payment.html', context)
        return render(request, 'expire.html', context)


class StripePaymentAPIView(APIView):
    """
    Create Payment intent
    """

    def post(self, request, *args, **kwargs):
        """
        """
        user = request.user
        serializer = PaymentIntentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # stripe payment
        stripe_obj = Stripe()
        resp = stripe_obj.create_payment_intent(
            user=user,
            amount=serializer.validated_data.get('amount'),
            currency=settings.DEFAULT_CURRENCY,
            service_type=serializer.validated_data.get("service_type"),
            recharge_number=serializer.validated_data.get("recharge_number"),
            recharge_type=serializer.validated_data.get("recharge_type"),
            service_provider=SERVICES_PROVIDER[0][0],
            recharge_transaction_id=serializer.validated_data.get('recharge_transaction_id')
        )
        return response(message=resp["detail"], status_code=resp['status_code'], data=resp["data"])


class StripeWebhookAPIView(APIView):
    """
    method for handle events on stripe
    """

    def post(self, request, *args, **kwargs):
        """
        """
        data = request.data
        webhook_obj = StripeWebhook()
        event_type = webhook_obj.get_event(data)
        if event_type:
            if event_type in ('payment_intent.succeeded',
                              'payment_intent.payment_failed', 'payment_intent.processing'):
                webhook_obj.connect_payment_update_hook(data)

        return Response(status=204)


# class PaymentListViewset(viewsets.ModelViewSet):
#     """
#     """
#     queryset = Orders.objects.filter()
#     serializer_class = InstructionSerializer
#     search_fields = ('key_text', 'customer__company')
#     permission_classes = (permissions.IsAuthenticated,)
#     ordering = ('-created_at',)
#     filter_fields = ('condition', 'applied_on', 'customer', 'action')
#
#     def filter_queryset(self, queryset):
#         queryset = super().filter_queryset(queryset)
#         queryset = queryset.filter(
#             coc_file_name__isnull=True
#         ).exclude(
#             applied_on=CustomerInstruction.TEST
#         )
#
#         return queryset
#
#     def perform_destroy(self, instance):
#         instance.is_deleted = True
#         instance.deleted_on = timezone.now()
#         instance.save()