from django import template
from preico import settings


register = template.Library()


@register.simple_tag()
def token_address():
    return settings.TOKEN_ADDRESS
