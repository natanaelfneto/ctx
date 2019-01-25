# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *


urlpatterns = [
    #
    url(r'login/$', LoginView.as_view(), name='login'),
    #
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    #
    url(r'add/$', AddUserView.as_view(), name='addUser'),
    #
    url(r'detail/(?P<pk>\d+)$', DetailUserView.as_view(), name='detailUser'),
    #
    url(r'list/$', ListUsersView.as_view(), name='listUsers'),
    #
    url(r'update/(?P<pk>\d+)/$', UpdateUserView.as_view(), name='updateUser'),
    #
    url(r'toggle-activation/(?P<pk>\d+)/$', ToggleActivationView.as_view(), name='toggleActivation'),
    #
    url(r'toggle-admin/(?P<pk>\d+)/$', ToggleAdminView.as_view(), name='toggleAdmin'),
    #
    url(r'toggle-superuser/(?P<pk>\d+)/$', ToggleSuperUserView.as_view(), name='toggleSuperUser'),
]

