from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db.models import Q
from django.views.generic import View, ListView, DetailView, UpdateView, TemplateView
from .models import CustomUser
from .forms import CustomUserProfileUpdateForm
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class UserStatusView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        if not (user.first_name or user.last_name) and user.picture:
            return redirect(f'/accounts/profile/{request.user.id}')
            # return reverse_lazy('update_profile')
        elif not user.kyc_verified:
            # return redirect(f'/accounts/kyc/{request.user.id}')
            return reverse_lazy('update_kyc')
        elif not user.phone_verified:
            # return redirect(f'/accounts/phone/{request.user.id}')
            return reverse_lazy('update_phone')
        else:
            return reverse('dashboard')


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'account/user_list.html'
    login_url = 'account_login'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/user_detail.html'
    login_url = 'account_login'


class UserUpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'picture']
    context_object_name = 'user'
    template_name = 'account/update_profile.html'
    login_url = 'account_login'
    success_url = reverse_lazy('update_profile')

    def get_object(self):
        return self.request.user


class UserUpdateKYCView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['kyc']
    context_object_name = 'user'
    template_name = 'account/update_kyc.html'
    login_url = 'account_login'
    success_url = reverse_lazy('update_kyc')

    def get_object(self):
        return self.request.user


class UserUpdatePhoneView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['phone']
    context_object_name = 'user'
    template_name = 'account/update_phone.html'
    login_url = 'account_login'
    success_url = reverse_lazy('update_phone')

    def get_object(self):
        return self.request.user


class SearchResultsListView(ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'account/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return CustomUser.objects.filter(
            Q(email__icontains=query) | Q(first_name__icontains=query) |
            Q(last_name__icontains=query) | Q(username__icontains=query)
        )


class DashboardView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        user = self.request.user
        if user.is_superuser and user.groups.filter(name='manager').exists():
            return 'accounts/manager/dashboard.html'
        elif user.is_staff and user.groups.filter(name='master').exists():
            return 'accounts/master/dashboard.html'
        elif user.is_active and user.groups.filter(name='member').exists():
            return 'accounts/member/dashboard.html'
        else:
            return '403.html'
