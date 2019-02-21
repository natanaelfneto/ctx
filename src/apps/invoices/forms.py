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
            'service_address',
            'equipment',
            'serial_number',
            'issue',
            'type_of_invoice',
            'invoice_description',
        ]

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.helper = InvoiceHelper()

    def save(self, commit=True):
        thisObject = super(InvoiceForm, self).save(commit=False)
        if commit:
            print(thisObject)
            thisObject.save()
            self.save_m2m()
        return thisObject