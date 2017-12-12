from django import template
from django.urls import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def can_refer(context):
    user = context.get('user')

    return ( user.is_authenticated
             and (user.first_name
                 and user.last_name
                 and ( user.profile and user.profile.wallet ) ) )

@register.simple_tag(takes_context=True)
def referral_code(context):
    user = context.get('user')
    result = ''

    if user.profile:
        result = user.profile.wallet

    return result


@register.simple_tag(takes_context=True)
def has_referral_code(context):
    user = context.get('user')

    return ( user.profile and user.profile.wallet )



@register.simple_tag(takes_context=True)
def referral_url(context):
    request = context.get('request')

    return request.build_absolute_uri(
        reverse( 'cp:auth-referred', kwargs={'referrer_code': referral_code(context), 'format': 'html'} ) )