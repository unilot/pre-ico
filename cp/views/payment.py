from rest_framework import generics, status
from rest_framework import permissions, response
from django.urls import reverse
from ..serializers import payment
from coinpayments.utils.api import APIClient


class CoinPayments(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = payment.CoinPayments

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = APIClient.get_client(
            str(request.build_absolute_uri(
                reverse('cp:payment-transaction-result',
                        kwargs={'user_id': user.id, 'format': 'json'}))
            )
        )

        result = client.createTransaction({
            'amount': serializer.data.get('amount'),
            'currency1': serializer.data.get('currency'),
            'currency2': serializer.data.get('currency'),
            'buyer_email': user.email,
            'buyer_name': '%s %s' % (user.first_name, user.last_name),
            'item_name': 'UNIT Tokens'
        })

        result['result']['currency'] = serializer.data['currency']

        return response.Response(data=result.get('result', {}), status=status.HTTP_200_OK)
