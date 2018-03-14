from rest_framework import generics, permissions, response
from django.urls import reverse
from django.utils.translation import ugettext as _

from coinpayments.utils.api import APIClient
from . import serializers

class Transaction(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.Transaction

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        input_data = request.data.dict()

        serializer = self.get_serializer(data=input_data)
        serializer.is_valid(raise_exception=True)

        client = APIClient.get_client(str(request.build_absolute_uri(
                                    reverse('coinpayments:transaction-callback',
                                        kwargs={'user_id': user.id, 'format': 'json'}))
                                ))

        result = client.createTransaction({
            'amount': serializer.data.get('amount'),
            'currency1': serializer.data.get('currency'),
            'currency2': serializer.data.get('currency'),
            'buyer_email': user.email,
            'buyer_name': '%s %s' % (user.first_name, user.last_name),
            'item_name': 'UNIT Tokens'
        })

        if result.get('error') != 'ok':
            raise RuntimeError(_('Failed to create transaction. Please try again later.'))

        serializer = self.get_serializer(data={**input_data, **result.get('result', {})})
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return response.Response(data=serializer.data)
