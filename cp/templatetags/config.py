from collections import OrderedDict

from django import template
from preico import settings
from django_countries.data import COUNTRIES


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
    return OrderedDict(
        (
            (key, COUNTRIES[key])
            if key not in settings.COUNTRIES_EXCLUDED else None
            for key in sorted(COUNTRIES, key=COUNTRIES.get) if not key in settings.COUNTRIES_EXCLUDED
        )
    )


@register.simple_tag()
def get_excluded_countries():
    return OrderedDict(
        (
            (key, COUNTRIES[key]) for key in sorted(settings.COUNTRIES_EXCLUDED)
        )
    )
