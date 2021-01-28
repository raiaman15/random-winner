from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Pool, InvestmentTransaction


class PoolListView(LoginRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    template_name = 'pools/pool_list.html'
    login_url = 'account_login'


class BookDetailView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DetailView):
    model = Pool
    context_object_name = 'pool'
    template_name = 'pools/pool_detail.html'
    login_url = 'account_login'
    permission_required = 'pool.special_status'


class SearchResultsListView(ListView):
    model = Pool
    context_object_name = 'pool_list'
    template_name = 'pools/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Pool.objects.filter(
            Q(name__icontains=query) | Q(master__icontains=query)
        )
