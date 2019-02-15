# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='mask')
def invoice_number_mask(value, arg):
    if str(arg) == "phone":
        masked_value = f'({value[0:1]}) {value[2:4]}-{value[5:7]}-{value[8:10]}'        
    elif str(arg) == "cnpj":
        masked_value = f'{value[0:1]}.{value[2:4]}.{value[5:7]}/{value[8:11]}-{value[12:13]}'
    else:
        masked_value = value

    return masked_value
        