from django import template
from django.utils.http import urlquote

from preico import settings


register = template.Library()


@register.simple_tag()
def facebook_page():
    return settings.SOCIAL_LINKS.get('FACEBOOK')


@register.simple_tag()
def twitter_channel():
    return settings.SOCIAL_LINKS.get('TWITTER')


@register.simple_tag()
def reddit_url():
    return settings.SOCIAL_LINKS.get('REDDIT')


@register.simple_tag()
def medium_blog():
    return settings.SOCIAL_LINKS.get('MEDIUM')


@register.simple_tag()
def telegram_channel():
    return settings.SOCIAL_LINKS.get('TELEGRAM')


@register.simple_tag()
def linkedin_company():
    return settings.SOCIAL_LINKS.get('LINKEDIN')


@register.simple_tag()
def slack_channel():
    return settings.SOCIAL_LINKS.get('SLACK')


@register.simple_tag()
def youtube_channel():
    return settings.SOCIAL_LINKS.get('YOUTUBE')


@register.simple_tag()
def github_organization():
    return settings.SOCIAL_LINKS.get('GITHUB')


@register.simple_tag()
def share_facebook(url):
    return 'https://www.facebook.com/sharer/sharer.php?u={0}' % urlquote(url)


@register.simple_tag()
def share_twitter(status):
    return 'https://twitter.com/home?status=%s' % (urlquote(status))


@register.simple_tag()
def share_reddit_post(title, url):
    return 'https://www.reddit.com/submit?title=%s&url=%s&sr=unilot_lottery&sendreplies=0'\
           % (urlquote(title), urlquote(url))


@register.simple_tag()
def share_telegram(url):
    return 'https://t.me/share/url?url=%s'% (urlquote(url))
