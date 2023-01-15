from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.serializers import PaymentIntentCreateSerializer
from apps.payment.utils.stripe import Stripe
from apps.payment.utils.webhooks import StripeWebhook


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
            # web_obj = StripeWebhook()
            # if (web_obj.retrive_invoice_detail(
            #     response['data']['metadata']['invoice_id'])):
            #     # cancel the intent
            #     context['paid'] = True
            #     if response['data'].get('status') != 'canceled':
            #         response = stripe_obj.cancel_payment_intent(
            #             intent_id=intent_id)

            print(response)
            if response.get('status') in ("requires_payment_method", "requires_source"):

                secret_id = response['client_secret']
                amount = response['metadata']['amount']
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
        serializer = PaymentIntentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # stripe payment
        stripe_obj = Stripe()
        response = stripe_obj.create_payment_intent(
            amount=serializer.validated_data.get('amount'),
            currency=settings.DEFAULT_CURRENCY,
        )
        return Response(response, response['status_code'])


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
            if event_type == 'account.updated':
                webhook_obj.connect_account_update_hook(data)
            elif event_type == 'payment_intent.succeeded':
                webhook_obj.connect_payment_update_hook(data)
            elif event_type == 'payment_intent.payment_failed':
                webhook_obj.connect_payment_update_hook(data)

        return Response(status=204)
