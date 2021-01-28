from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import TemplateView


class CompanyPageView(TemplateView):
    template_name = 'pages/company.html'


class ProductPageView(TemplateView):
    template_name = 'pages/product.html'
