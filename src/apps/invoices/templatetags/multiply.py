# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return f"{float(value*arg):.2f}"