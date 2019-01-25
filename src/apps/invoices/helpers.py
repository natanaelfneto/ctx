# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit


class InvoiceHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InvoiceHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('date', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('client', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('address', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('equipment', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('issue', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('type_of_invoice', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('invoice_description', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('displacement', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('time', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('supplies', css_class="form-control"),
                css_class="form-group"
            ),
            Submit('submit', 'Submit')
        )
