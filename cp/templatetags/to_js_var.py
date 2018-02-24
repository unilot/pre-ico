from django import template

register = template.Library()


@register.simple_tag()
def js_render_var(name):
    return '{{:%s}}'%name
