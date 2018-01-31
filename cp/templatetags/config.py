from django import template
from preico import settings
from phonenumbers.phonenumberutil import COUNTRY_CODE_TO_REGION_CODE

from preico.utils import (get_investing_countries, get_none_investing_countries,
                          get_phone_codes as u_get_phone_codes, get_wallet_app_choice)

register = template.Library()


@register.simple_tag()
def token_address():
    return settings.TOKEN_ADDRESS

@register.simple_tag()
def token_price():
    return '{:f}'.format(settings.TOKEN_SETTINGS['PRICE'])


@register.simple_tag()
def token_bonus():
    return ( settings.TOKEN_SETTINGS['BONUS'] * 100 )


@register.simple_tag()
def token_cap():
    return settings.TOKEN_SETTINGS['CAP']


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
            result = 'and %s' % country
            first = False
        else:
            result = '%s, %s' % (country, result)

    return result


@register.simple_tag()
def get_phone_codes():
    return u_get_phone_codes().items()


@register.simple_tag()
def get_wallet_apps():
    return get_wallet_app_choice()
