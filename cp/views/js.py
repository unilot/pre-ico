from rest_framework import views, response, permissions

from console.models import ExchangeRate
from preico.rest_framework import renderers
from preico.settings import TOKEN_SETTINGS


class ConfigJsView(views.APIView):
    permission_classes = [ permissions.AllowAny ]
    template_name = 'js/config.js'
    renderer_classes = (renderers.JSRenderer,)

    def get(self, request, *args, **kwargs):
        exchange_rate = ExchangeRate.objects.order_by('created_at').last()
        amount_raised = int(exchange_rate.total_tokens) - int(exchange_rate.tokens_left)

        data = {
            'eth': {
                'fiatExchangeRate': '{:f}'.format(exchange_rate.rate)
            },
            'token': {
                'price': '{:f}'.format(TOKEN_SETTINGS.get('PRICE')),
                'bonus': '{:f}'.format(TOKEN_SETTINGS.get('BONUS', 0)),
                'cap': '%d' % (int(TOKEN_SETTINGS.get('CAP', 0)/1.5))
            },
            'sale_progress': '{:f}'.format(amount_raised / int(exchange_rate.total_tokens)),
            'sale_amount': '{:f}'.format(int(exchange_rate.eth_raised) / (10**18))
        }

        return response.Response(data=data, content_type='application/javascript')
