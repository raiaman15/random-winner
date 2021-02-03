from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView
from .models import Pool, InvestmentTransaction


class PoolCreateView(LoginRequiredMixin, CreateView):
    model = Pool
    template_name = 'pools/pool_create.html'
    fields = ['name', 'size', 'investment']

    def form_valid(self, form):
        form.instance.master = self.request.user
        return super(PoolCreateView, self).form_valid(form)


class PoolListView(LoginRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    template_name = 'pools/pool_list.html'
    login_url = 'account_login'


class PoolDetailView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DetailView):
    model = Pool
    context_object_name = 'pool'
    template_name = 'pools/pool_detail.html'
    login_url = 'account_login'


class SearchResultsListView(ListView):
    model = Pool
    context_object_name = 'pool_list'
    template_name = 'pools/pool_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Pool.objects.filter(Q(name__icontains=query))
