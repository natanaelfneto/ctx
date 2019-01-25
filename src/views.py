# -*- coding: utf-8 -*-
# django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, RedirectView
from django.views.generic.base import TemplateView
# self imports

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    page_title = "Index"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title

        return context