# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit


class UserHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(UserHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('email', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('password1', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('password2', css_class="form-control"),
                css_class="form-group"
            ),
            Submit('submit', 'Submit')
        )
