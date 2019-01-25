# -*- coding: utf-8 -*-
import re

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, validators

from .models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        self.user = authenticate(None, username=attrs.get('email', None), password=attrs.get('password', None))
        if not self.user:
            raise validators.ValidationError('Invalid')

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    class Meta:
        model = BasicUser
        fields = ('active','admin','asymmetric_pair','email','signer_device','user_pin','superuser')
