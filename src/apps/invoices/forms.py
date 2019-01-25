# -*- coding: utf-8 -*-
from django import forms

from .helpers import *
from .models import *
 

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'date',
            'client',
            'equipment',
            'issue',
            'type_of_invoice',
            'invoice_description',
            'displacement',
            'time',
            'supplies'
        ]

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.helper = InvoiceHelper()

    def save(self, commit=True):
        thisObject = super(InvoiceForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject