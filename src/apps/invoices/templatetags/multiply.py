# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    value = float(value) if value is not None else 0
    arg = float(arg) if arg is not None else 0
    return f"{float(value*arg):.2f}"