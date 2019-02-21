# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='mask')
def mask(value, arg):
    if str(arg) == "phone":
        print(len(value))
        if len(value) == 10:
            masked_value = f'({value[0:2]}) {value[2:6]}-{value[6:]}'        
        elif len(value) == 11:
            masked_value = f'({value[0:2]}) {value[2:5]}-{value[5:8]}-{value[8:]}'        
        else:
            masked_value = 'oq?'
    elif str(arg) == "cnpj":
        masked_value = f'{value[0:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}'
    elif str(arg) == "cep":
        masked_value = f'{value[0:2]}.{value[2:5]}-{value[5:]}'
    elif str(arg) == "value":
        masked_value = f'R$ {float(value):.2f}'
    else:
        masked_value = value

    return masked_value
        