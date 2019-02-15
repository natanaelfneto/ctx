# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='invoice_number_mask')
def invoice_number_mask(value, arg):
    if str(arg) == "Contrato":
        return f"C{int(value):03d}"
    elif str(arg) == "Fatura":
        return f"F{int(value):03d}"
    elif str(arg) == "Garantia":
        return f"G{int(value):03d}"
    elif str(arg) == "Instalação":
        return f"I{int(value):03d}"
        
    