from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import TemplateView
from django.shortcuts import redirect


class CompanyPageView(TemplateView):
    """ The Product Page is acting as Company Page since it is a product based company """
    # template_name = 'pages/company.html'

    def dispatch(self, request):
        return redirect('product_page')


class ProductPageView(TemplateView):
    template_name = 'pages/product.html'
