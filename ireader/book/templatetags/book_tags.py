# -*- coding:utf -*-

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('tags/list_render_tag.html')
def list_render(l, t, c):
    return {
        'list': l,
        'title': t,
        'category_index': c,
        'settings': settings
    }
