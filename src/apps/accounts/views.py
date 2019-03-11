# -*- coding: utf-8 -*-
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.http import is_safe_url
from django.views.generic import FormView, RedirectView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from rest_framework import permissions, renderers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .serializers import *


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

    def form_valid(self, form):
        if form.is_valid():
            if not form.cleaned_data['remember_me']:
                self.request.session.set_expiry(0)
            login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

        
# Users Classes
class AddUserView(LoginRequiredMixin, CreateView):
    template_name = 'accounts_add.html'
    page_title = "Usuário"
    model = BasicUser
    form_class = UserForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(BaseFormView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title

        return context


class DetailUserView(DetailView):
    template_name = 'accounts_detail.html'
    page_title = "User"
    model = BasicUser


class ListUsersView(LoginRequiredMixin, TemplateView):
    template_name = "accounts_list.html"
    page_title = "Usuários"
    model = BasicUser
    queryset = BasicUser.objects.filter()


class UpdateUserView(LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        if request.POST.get('reset', None) == 'Remove':
            self.get_object().delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return super(UpdateUserView, self).post(request, *args, **kwargs)


class ToggleActivationView(RedirectView):
    url = '/'

    def get(self, *args, **kwargs):
        basic_user = get_object_or_404(BasicUser, pk=kwargs['pk'])
        basic_user.active = not basic_user.active
        basic_user.save()
        return super(ToggleActivation, self).get(*args, **kwargs)


class ToggleAdminView(RedirectView):
    url = '/'

    def get(self, *args, **kwargs):
        basic_user = get_object_or_404(BasicUser, pk=kwargs['pk'])
        basic_user.admin = not basic_user.admin
        basic_user.save()
        return super(ToggleAdmin, self).get(*args, **kwargs)


class ToggleSuperUserView(RedirectView):
    url = '/'

    def get(self, *args, **kwargs):
        basic_user = get_object_or_404(BasicUser, pk=kwargs['pk'])
        basic_user.superuser = not basic_user.superuser
        basic_user.save()
        return super(ToggleSuperUser, self).get(*args, **kwargs)