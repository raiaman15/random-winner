from django.db.models import Q
from django.views.generic import CreateView, ListView, DetailView
from .models import Pool, InvestmentTransaction
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)
from braces.views import GroupRequiredMixin


class PoolCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Pool
    template_name = 'pools/pool_create.html'
    fields = ['name', 'size', 'investment']
    group_required = u"master"

    def form_valid(self, form):
        form.instance.master = self.request.user
        return super(PoolCreateView, self).form_valid(form)


class PoolListView(LoginRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    template_name = 'pools/pool_list.html'
    login_url = 'account_login'
    group_required = [u"member", u"master", u"admins"]


class PoolDetailView(LoginRequiredMixin, DetailView):
    model = Pool
    context_object_name = 'pool'
    template_name = 'pools/pool_detail.html'
    login_url = 'account_login'
    group_required = [u"member", u"master", u"admins"]


class SearchResultsListView(LoginRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    template_name = 'pools/pool_list.html'
    group_required = [u"member", u"master", u"admins"]

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Pool.objects.filter(Q(name__icontains=query))
