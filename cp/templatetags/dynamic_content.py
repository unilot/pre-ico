from django import template
from django.utils.safestring import mark_safe
from martor.utils import markdownify
from .. import models


register = template.Library()


@register.simple_tag()
def content_text(key):
    keys = key.split(',')
    texts_qs = models.Text.objects.language() \
        .filter(key__in=list(keys))
    result = {}

    if len(keys) > 1:
        texts = texts_qs.all()

        for text in texts:
            result[text.key.replace('-', '_')] = mark_safe(markdownify(text.text))
    else:
        try:
            text = texts_qs.get()

            result = mark_safe(markdownify(text.text))
        except models.Text.DoesNotExist as error:
            result = ''

    return result
