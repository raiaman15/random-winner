from django.views.generic import TemplateView
from django.shortcuts import redirect


class CompanyPageView(TemplateView):
    """ The Product Page is acting as Company Page since it is a product based company """
    # template_name = 'pages/company.html'
    template_name = 'pages/product.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('status')
        return super(CompanyPageView, self).dispatch(request, *args, **kwargs)


class ProductPageView(TemplateView):
    template_name = 'pages/product.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('status')
        return super(ProductPageView, self).dispatch(request, *args, **kwargs)
