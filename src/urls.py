# -*- coding: utf-8 -*-
# django imports
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

# apps imports
from invoices.views import *

# self imports
from .views import *

# set site header
admin.site.site_header = settings.NAME

urlpatterns = [

    #
    # url(r'^$', IndexView.as_view(), name='index'),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('invoice_list'), permanent=False), name='index'),

    # app accounts
    url(r'^accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    #
    url(r'invoice/add/$', InvoiceAddView.as_view(), name='invoice_add'),

    #
    url(r'^invoice/$', InvoiceListView.as_view(), name='invoice_list'),

    #
    url(r'^invoice/(?P<pk>\d+)/$', InvoiceDetailView.as_view(), name='invoice_detail'),

    #
    url(r'^invoice/status/update$', InvoiceStatusUpdateView.as_view(), name='invoice_status_update'),

    #
    url(r'^invoice/supplies/update$', InvoiceSuppliesUpdateView.as_view(), name='invoice_supplies_update'),

    #
    url(r'^invoice/(?P<pk>\d+)/delete/$', InvoiceDeleteView.as_view(), name='invoice_delete'),

    # app admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)