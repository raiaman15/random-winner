from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import TemplateView


class CompanyPageView(TemplateView):
    template_name = 'pages/company.html'


class ProductPageView(TemplateView):
    template_name = 'pages/product.html'


class DashboardView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        user = self.request.user
        if user.is_superuser and user.groups.filter(name='manager').exists():
            return 'pages/manager/dashboard.html'
        elif user.is_staff and user.groups.filter(name='master').exists():
            return 'pages/master/dashboard.html'
        elif user.is_active and user.groups.filter(name='member').exists():
            return 'pages/member/dashboard.html'
        else:
            return 'pages/complete-kyc.html'
