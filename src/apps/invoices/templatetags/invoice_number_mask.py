# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='invoice_number_mask')
def invoice_number_mask(value):
    return f"{int(value):06d}"