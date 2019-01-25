# -*- coding: utf-8 -*-
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class SuperUser(BaseUserManager):
    def create_superuser(self, email, password):
        super_user = self.model(
            email=email,
            superuser=True,
            admin=True
        )
        super_user.set_password(password)
        super_user.save(using=self.db)

        return super_user


class BasicUser(AbstractBaseUser, PermissionsMixin):
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)
    # Super user need
    superuser = models.BooleanField(default=False)
    objects = SuperUser()

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'basic_users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __unicode__(self):
        return self.email

    @property
    def is_active(self):
        return self.active == 1

    @property
    def is_staff(self):
        return self.active == 1

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def get_short_name(self):
        return self.email
