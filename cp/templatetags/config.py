from django import template
from django.utils.translation import ugettext as _
from preico import settings

from preico.utils import (get_investing_countries, get_none_investing_countries,
                          get_wallet_app_choice)
from datetime import datetime, timezone, timedelta

register = template.Library()


@register.simple_tag()
def token_address():
    return settings.TOKEN_ADDRESS

@register.simple_tag()
def token_price():
    return '{:f}'.format(settings.TOKEN_SETTINGS['PRICE'])


@register.simple_tag()
def token_coin_price(coin):
    return '{:.9f}'.format(settings.TOKEN_SETTINGS['COIN_PRICE'].get(coin, 0))


@register.simple_tag()
def token_coin_min_amount(coin):
    return '{:f}'.format(
        settings.TOKEN_SETTINGS['COIN_PRICE'].get(coin, 0) * settings.TOKEN_SETTINGS['MIN_CAP'].get(coin, 0)
    )


@register.simple_tag()
def token_bonus():
    return ( settings.TOKEN_SETTINGS['BONUS'] * 100 )


@register.simple_tag()
def token_cap():
    return settings.TOKEN_SETTINGS['CAP']

@register.simple_tag()
def token_eth_cap():
    return settings.TOKEN_SETTINGS['ETH_CAP']

@register.simple_tag()
def get_countries():
    return get_investing_countries()


@register.simple_tag()
def get_excluded_countries():
    return get_none_investing_countries()


@register.simple_tag()
def get_excluded_countries_as_listed_text():
    result = ''

    first = True

    for key, country in get_none_investing_countries().items():
        if first:
            result = '%s %s' % (_('and'), country)
            first = False
        else:
            result = '%s, %s' % (country, result)

    return result

@register.simple_tag()
def get_wallet_apps():
    return get_wallet_app_choice()


@register.simple_tag()
def get_humanized_token_amount(token_balance):
    if not token_balance:
        return 0

    return float( int( token_balance ) / ( 10**18 ) )


@register.simple_tag()
def get_stage_start_date(stage):
    index = int(stage)
    stages = (
        datetime(2018, 1, 10, 19, 0, tzinfo=timezone.utc),
        datetime(2018, 2, 22, 19, 0, tzinfo=timezone.utc),
        datetime(2018, 4, 20, 19, 0, tzinfo=timezone.utc),
    )

    if index >= len(stages):
        raise RuntimeError('Invalid stage %s' % stage)

    return stages[index]


@register.simple_tag()
def get_stage_end_date(stage):
    index = int(stage)
    stages = (
        datetime(2018, 2, 17, 19, 0, tzinfo=timezone.utc),
        datetime(2018, 3, 22, 19, 0, tzinfo=timezone.utc),
        datetime(2018, 5, 20, 19, 0, tzinfo=timezone.utc),
    )

    if index >= len(stages):
        raise RuntimeError('Invalid stage %s' % stage)

    return stages[index]

@register.filter()
def add_days(value, days):
    return value + timedelta(days=days)
