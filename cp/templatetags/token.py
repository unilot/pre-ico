from django import template
from preico import settings
from django.utils import timezone
from console.models import ExchangeRate


register = template.Library()

exchange_rates = {}
exchange_last_request = None


@register.simple_tag()
def token_address():
    return settings.TOKEN_ADDRESS


@register.simple_tag()
def token_price():
    return '{:f}'.format(settings.TOKEN_SETTINGS['PRICE'])


@register.simple_tag()
def token_coin_price(coin):
    if str(coin).upper() == 'ETH':
        price = settings.TOKEN_SETTINGS.get('PRICE')
    else:
        price = settings \
                   .TOKEN_SETTINGS.get('COINS', {}) \
                   .get(coin, {}) \
                   .get('PRICE', 0)

    return '{:.9f}'.format(price)


@register.simple_tag()
def token_coin_fiat_rate(coin):
    now = timezone.now()

    if not exchange_last_request or (now - exchange_last_request) >= timezone.timedelta(minutes=10):
        rates = ExchangeRate.objects.distinct('currency').order_by('currency', '-created_at')

        for e_rate in rates:
            exchange_rates[e_rate.currency] = e_rate.rate

    return exchange_rates.get(coin, 0)


@register.simple_tag()
def token_coin_name(coin):
    return settings \
               .TOKEN_SETTINGS.get('COINS', {}) \
               .get(coin, {}) \
               .get('NAME', '')


@register.simple_tag()
def token_coin_has_icon(coin):
    return settings \
               .TOKEN_SETTINGS.get('COINS', {}) \
               .get(coin, {}) \
               .get('HAS_ICON', False)


@register.simple_tag()
def token_coin_min_num_tokens(coin):
    if str(coin).upper() == 'ETH':
        result = 1
    else:
        result = settings \
            .TOKEN_SETTINGS.get('COINS', {}) \
            .get(coin, {}) \
            .get('MIN_CAP', 0)


    return result


@register.simple_tag()
def token_coin_min_amount(coin):
    coin_data = settings \
        .TOKEN_SETTINGS.get('COINS', {}) \
        .get(coin, {})

    return '{:f}'.format(coin_data.get('PRICE', 0) * coin_data.get('MIN_CAP', 0))

@register.simple_tag()
def token_coins():
    return settings.TOKEN_SETTINGS.get('COINS', {}).keys()


@register.simple_tag()
def token_bonus():
    return (settings.TOKEN_SETTINGS['BONUS'] * 100)


@register.simple_tag()
def token_cap():
    return settings.TOKEN_SETTINGS['CAP']


@register.simple_tag()
def token_eth_cap():
    return settings.TOKEN_SETTINGS['ETH_CAP']

@register.simple_tag()
def get_humanized_token_amount(token_balance):
    if not token_balance:
        return 0

    return float( int( token_balance ) / ( 10**18 ) )
