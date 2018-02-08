from django import template
from django.urls import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def can_refer(context):
    user = context.get('user')

    return ( user.is_authenticated
             and ( user.profile and user.profile.referral_code ) )

@register.simple_tag(takes_context=True)
def referral_code(context):
    user = context.get('user')
    result = ''

    if user.profile:
        result = user.profile.referral_code

    return result


@register.simple_tag(takes_context=True)
def has_referral_code(context):
    user = context.get('user')

    return ( user.profile and user.profile.wallet )



@register.simple_tag(takes_context=True)
def referral_url(context):
    request = context.get('request')

    return request.build_absolute_uri(
        reverse( 'landing:index-html-referred', kwargs={'referrer_code': referral_code(context)} ) )


#TODO Not sure it should be here
@register.simple_tag(takes_context=True)
def main_page_url(context):
    return reverse('landing:index-html')


@register.simple_tag()
def contribute_url():
    return reverse('cp:sign-up', kwargs={'format': 'html'})
