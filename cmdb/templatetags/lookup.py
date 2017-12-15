# -*- coding: utf-8 -*-

from django import template

register = template.Library()
@register.filter
def lookup(d, key):
    return d[key]

@register.filter
def multiply(value, arg):
    return value*arg
