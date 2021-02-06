from django.db.models import Q
from django.utils import timezone
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
        """ Creates only if the Master of Pool is verified by Manager
        and if the investment amount is a multiple of a decided amount.
        Generates codename (Limits 1 pool creation per day)
        """
        form.instance.master = self.request.user
        prefix = self.request.user.username[:3]
        t = timezone.now()
        yy = t.strftime("%Y")
        mm = t.strftime("%m")
        dd = t.strftime("%d")
        # A Master can create only 1 pool per day
        # hh = t.strftime("%H")
        # mm = t.strftime("%M")
        form.instance.codename = prefix+yy+mm+dd  # +hh+mm
        return super(PoolCreateView, self).form_valid(form)


class PoolListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    template_name = 'pools/pool_list.html'
    login_url = 'account_login'
    group_required = [u"member", u"master", u"manager"]


class PoolDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Pool
    context_object_name = 'pool'
    template_name = 'pools/pool_detail.html'
    login_url = 'account_login'
    group_required = [u"member", u"master", u"manager"]


class PoolSearchView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    template_name = 'pools/pool_list.html'
    group_required = [u"member", u"master", u"manager"]

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Pool.objects.filter(Q(name__icontains=query))
