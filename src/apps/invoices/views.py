# -*- coding: utf-8 -*-
#django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView


# self import
from accounts.models import *
from .forms import *
from .models import *


# INVOICES
class InvoiceAddView(LoginRequiredMixin, CreateView):
    template_name = 'invoice_add.html'
    page_title = "Signed Data"
    success_url = '/invoice/'
    model = Invoice
    form_class = InvoiceForm

    def form_valid(self, form):
        if self.request.user.is_active:
            basic_user = get_object_or_404(BasicUser, pk=self.request.user.id)
            invoice = form.save()
            total_value = 0
            for supply in invoice.supplies.all():
                total_value = total_value + int(get_object_or_404(Supply, description=supply).value)
            invoice.total_value = total_value + (invoice.displacement * 250)
            invoice.created_by = basic_user
            invoice.save()
            self.success_url += str(invoice.id)

            return HttpResponseRedirect(self.success_url)

        return super(InvoiceAddView, self).get(form)

    def get_context_data(self, **kwargs):
        context = super(InvoiceAddView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class InvoiceListView(LoginRequiredMixin, ListView):
    template_name = "invoice_list.html"
    page_title = "Lista de Ordens de Serviço"
    model = Invoice
    queryset = list(reversed(Invoice.objects.filter()))
    form = []
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class InvoiceDetailView(DetailView):
    template_name = 'invoice_detail.html'
    page_title = "Vizualizar Ordem de Serviço"
    model = Invoice

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

