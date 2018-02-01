import re

from django import template
from preico import  utils


register = template.Library()


@register.simple_tag()
def get_phone_codes():
    return utils.get_phone_codes().items()

@register.simple_tag()
def get_phone_code(phone_number):
    phone_codes = utils.get_phone_codes()

    if not phone_number:
        return ''

    for code, label in phone_codes.items():
        if re.sub('[^\d]', '', phone_number)[:len(str(code))] == str(code):
            return code

    return ''

@register.simple_tag()
def get_phone_without_code(phone_number):
    if not phone_number:
        return ''

    code = get_phone_code(phone_number)
    return re.sub('[^\d]', '', phone_number)[len(str(code)):]

