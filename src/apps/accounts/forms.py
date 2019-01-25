# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate

from .helpers import *
from .models import *


class LoginForm(forms.Form):
    email = forms.EmailField(label='email', required=True)
    password = forms.CharField(label='Senha', required=True)
    remember_me = forms.BooleanField(label="Remember me", required=False)

    def clean(self):
        if self.errors:
            return super(LoginForm, self).clean()

        user = BasicUser.objects.filter(email=self.cleaned_data['email'])
        self.user = authenticate(username=self.cleaned_data.get('email', None), password=self.cleaned_data['password'])

        if user.count() == 0:
            self.add_error('email', u'Invalid parameters')

        if (not self.user or not self.user.active == 1) and self.cleaned_data.get('email', None):
            self.add_error('password', u'Invalid parameters')

        return super(LoginForm, self).clean()

    def get_user(self):
        return self.user


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label=u'Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = BasicUser
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = UserHelper()

        if self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        print (self.cleaned_data["password2"])
        if password1 != password2:
            raise forms.ValidationError(u"Password Invalid")
            return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)

        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
