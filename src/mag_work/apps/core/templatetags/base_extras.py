# -*- coding:utf-8 -*-
from django import template
from django.core.urlresolvers import reverse, resolve, Resolver404


register = template.Library()

@register.assignment_tag(takes_context=True)
def check_urls(context, type):
    URLS = {
        u'LOGIN': (u'login',),
        u'REGISTER': (u'registration',),
    }
    request = context.get('request')
    if type and request:
        try:
            current_url = resolve(request.path_info).url_name
            return True if current_url in URLS[type] else False
        except Resolver404:
            return False
    return False