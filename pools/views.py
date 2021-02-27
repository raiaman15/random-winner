from django.db.models import Q
from django.http.response import HttpResponse
from django.utils import timezone
from django.views.generic import View, CreateView, ListView, DetailView
from .models import Pool, PoolInvite
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from config.messages import response_messages


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
        prefix = self.request.user.username
        t = timezone.now()
        yy = t.strftime("%Y")
        mm = t.strftime("%m")
        dd = t.strftime("%d")
        # A Master can create only 1 pool per day
        # hh = t.strftime("%H")
        # mm = t.strftime("%M")
        if Pool.objects.filter(codename=prefix+yy+mm+dd).exists():
            messages.error(self.request, response_messages['pool_creation_limit_exceeded'])
            return super(PoolCreateView, self).get(self.request)
        else:
            form.instance.codename = prefix+yy+mm+dd  # +hh+mm
        return super(PoolCreateView, self).form_valid(form)


class PoolListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    paginate_by = 100
    template_name = 'pools/pool_list.html'
    login_url = 'account_login'
    group_required = [u"member", u"master"]


class PoolMembershipListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    paginate_by = 100
    template_name = 'pools/pool_list.html'
    login_url = 'account_login'
    group_required = [u"member", u"master"]

    def get_queryset(self):
        username = self.request.user.username
        return get_object_or_404(get_user_model(), username=username).member_of_pool.all()


class PoolMastershipListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    paginate_by = 100
    template_name = 'pools/pool_list.html'
    login_url = 'account_login'
    group_required = [u"member", u"master"]

    def get_queryset(self):
        username = self.request.user.username
        return get_object_or_404(get_user_model(), username=username).master_of_pool.all()


class PoolDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Pool
    context_object_name = 'pool'
    template_name = 'pools/pool_detail.html'
    login_url = 'account_login'
    group_required = [u"member", u"master"]

    # Pool Details visible to owners only
    # def get(self, request, *args, **kwargs):
    #     # pool = get_object_or_404(self.model, id=self.kwargs['pk'])
    #     # if pool.is_member(request.user) or pool.is_master(request.user):
    #     #     return super(PoolDetailView, self).get(request, *args, **kwargs)
    #     # else:
    #     #     messages.error(request, 'You cannot access details. You can only join the pool. Reason: The pool is not yours')
    #     #     return redirect('pool_list')
    #     return super(PoolDetailView, self).get(request, *args, **kwargs)


class PoolSearchView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Pool
    context_object_name = 'pool_list'
    paginate_by = 100
    template_name = 'pools/pool_list.html'
    group_required = [u"member", u"master", u"manager"]

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Pool.objects.filter(Q(name__icontains=query))


# Pool Invite

class PoolInviteCreateView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = [u"member", u"master"]

    def post(self, request):
        pool_id = int(request.POST.get('pool'))
        pool = get_object_or_404(Pool, id=pool_id)
        if pool.is_master(request.user):
            invited = []
            usernames = str(request.POST.get('contact_numbers')).strip().replace(' ', '').split(',')
            remaining_invites = pool.size - pool.invitations.count()
            for username in usernames[:remaining_invites]:
                try:
                    pool.invite(username)
                    invited.append(username)
                except Exception as e:
                    messages.error(request, f'Unable to invite {username}! Error: {e}')
            messages.success(request, f'Invitations to {", ".join(invited)} sent successfully')
        return redirect('status')


class PoolInviteListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = PoolInvite
    context_object_name = 'pool_invite_list'
    paginate_by = 100
    template_name = 'pools/pool_invite_list.html'
    login_url = 'account_login'
    group_required = [u"member", u"master"]

    def get_queryset(self):
        username = self.request.user.username
        return PoolInvite.objects.filter(username=username)


# Pool Join & Exit

class PoolJoinView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = [u"member", u"master"]

    def post(self, request):
        accept_reject = str(request.POST.get('accept_reject'))
        pool_id = int(request.POST.get('pool'))
        pool = get_object_or_404(Pool, id=pool_id)

        if accept_reject in ('Accept', 'Reject'):
            if accept_reject == 'Accept':
                self.request.user.refresh_balance_investment()
                if pool.investment > self.request.user.balance_amount:
                    remaining_amount = pool.investment - self.request.user.balance_amount
                    messages.warning(request, f'Please add ₹ {remaining_amount} to your account.')
                    return redirect('profile_balance_transaction_create')
                if not self.user.billing_address:
                    messages.warning(request, response_messages['profile_billing_address_incomplete'])
                    return redirect('profile_billing_address_create')
                if not self.user.bank_account_detail:
                    messages.warning(request, response_messages['profile_bank_account_detail_incomplete'])
                    return redirect('profile_bank_account_detail_create')
                try:
                    pool.join(request.user)
                    messages.success(request, f'You have joined the pool - {pool.name}')
                    PoolInvite.objects.filter(pool=pool, username=request.user.username).delete()
                except Exception as e:
                    messages.error(request, f'Unable to join the pool. Error: {e}')
            else:
                try:
                    PoolInvite.objects.filter(pool=pool, username=request.user.username).delete()
                except Exception as e:
                    messages.error(request, f'Unable to join the pool. Error: {e}')
        else:
            messages.error(request, 'Your response is invalid. Please try again!')
        return redirect('pool_invite_list')


# Automatic Schedule: Activate Pools, Spin, Exit PoolMember
class AutomaticActivateScheduleView(View):
    def get(self, request):
        now = timezone.now()
        start = timezone.now().replace(day=2, hour=00, minute=00)
        end = timezone.now().replace(day=28, hour=23, minute=59)
        activated_count = 0
        failed_count = 0
        if now > start and now < end:
            pools = Pool.objects.all()
            for pool in pools:
                if not pool.activated:
                    try:
                        pool.activate()
                        activated_count += 1
                    except Exception as e:
                        failed_count += 1

        return HttpResponse(f'{activated_count} Pools Activated. {failed_count} Pools Failed Activation.')


class AutomaticSpinScheduleView(View):
    def get(self, request):
        # active_pool_count = Pool.objects.exclude(activated__isnull=True).count()
        now = timezone.now()
        start = timezone.now().replace(day=1, hour=00, minute=00)
        end = timezone.now().replace(day=28, hour=00, minute=00)
        spinned_count = 0
        failed_count = 0
        if now > start and now < end:
            pools = Pool.objects.all()
            for pool in pools:
                try:
                    pool.spin()
                    spinned_count += 1
                except Exception as e:
                    failed_count += 1

        return HttpResponse(f'{spinned_count} Pools Spinned. {failed_count} Pools Failed Spinning.')
