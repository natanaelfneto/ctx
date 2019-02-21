# -*- coding: utf-8 -*-
#python imports
import datetime
import json
import pytz

#django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView

# self import
from accounts.models import *
from .forms import *
from .models import *


# INVOICES
class InvoiceAddView(LoginRequiredMixin, CreateView):
    template_name = 'invoice_add.html'
    page_title = "Signed Data"
    success_url = reverse_lazy('invoice_list')
    model = Invoice
    form_class = InvoiceForm

    def form_valid(self, form):
        if self.request.user.is_active:
            basic_user = get_object_or_404(BasicUser, pk=self.request.user.id)
            invoice = form.save()
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
    queryset = Invoice.objects.filter()
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


class InvoiceStatusUpdateView(TemplateView):

    def post(self, request, *args, **kwargs):
        # check if user is active
        if self.request.user.is_active:
            # get data from post body
            data = json.loads(request.body)
            # get current invoice object
            invoice = get_object_or_404(Invoice, pk=data['pk'])
            # update invoice status
            invoice.status = data['status']
            # save it
            invoice.save()

        return HttpResponse()


class InvoiceSuppliesUpdateView(TemplateView):

    def post(self, request, *args, **kwargs):
        # check if user is active
        if self.request.user.is_active:
            # get data from post body
            data = json.loads(request.body)
            # aux variable for suppy
            supply = data['supply']
            # get current invoice object
            invoice = get_object_or_404(Invoice, pk=data['pk'])
            # check type of data was sent
            if data['type'] == 'addNewSupply':
                # strip day, month and year from date
                print(supply['date'])
                supply_day = str(supply['date'])[0:2]
                supply_month = str(supply['date'])[3:5]
                supply_year = str(supply['date'])[6:10]
                # format a string as a raw date
                raw_date = f'{supply_year}-{supply_month}-{supply_day}'
                # parse raw date string as date variable
                date = datetime.datetime.strptime(raw_date, '%Y-%m-%d')
                # make date timezone aware
                aware_date = pytz.utc.localize(date)
                # set up supply object
                supply = Supply(
                    date=aware_date,
                    description=supply['description'],
                    amount=supply['amount'],
                    value=supply['value'],
                    invoice_parent=invoice
                )
                # save it
                supply.save()
                # filter all supplies with current invoice as foreign key
                supplies = Supply.objects.filter(invoice_parent=invoice)
                # loop through found supplies
                for supply in supplies:
                    # set it as a m2m relation
                    invoice.supplies.add(supply.id)
            elif data['type'] == 'removeSupply':
                # get supply object to be removed
                supply = get_object_or_404(Supply, pk=supply['pk'])
                # delete object from database
                supply.delete()
                # remove m2m relation to invoice object
                invoice.supplies.remove(supply.id)
            else:
                return HttpResponse()    
            # update the invoice total value
            invoice.total_value = float(data['total_value'])
            # save it
            invoice.save()
            # json response
            return HttpResponse()


class InvoiceDeleteView(DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice_list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)