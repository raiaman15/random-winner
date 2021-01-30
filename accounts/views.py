from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db.models import Q
from django.views.generic import View, ListView, DetailView, UpdateView, TemplateView
from .models import CustomUser, ContactNumberOTP
from .forms import CustomUserProfileUpdateForm
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse


class UserStatusView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        if not ((user.first_name or user.last_name) and user.picture):
            return redirect('profile')
        elif not user.identity_verified:
            return redirect('identity')
        elif not user.contact_verified:
            return redirect('contact')
        else:
            return redirect('dashboard')


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


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'picture']
    context_object_name = 'user'
    template_name = 'account/profile.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class UserIdentityView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['aadhaar_number', 'identity_proof']
    context_object_name = 'user'
    template_name = 'account/identity.html'
    login_url = 'account_login'
    success_url = reverse_lazy('identity')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class UserContactView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['contact_number']
    context_object_name = 'user'
    template_name = 'account/contact.html'
    login_url = 'account_login'

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def get_success_url(self):
        if not self.request.user.generate_otp():
            return HttpResponse('You requested for an OTP within last 5 minutes. Please try again later!')
        return reverse_lazy('contact_confirm')


class UserContactConfirmView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/contact_confirm.html'
    login_url = 'account_login'
    success_url = reverse_lazy('contact_confirm')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request):
        if request.user.contact_verified:
            return redirect('contact')

        user_otp = 0
        if isinstance(request.POST.get("otp_confirm"), str):
            if len(request.POST.get("otp_confirm")) == 6:
                user_otp = int(request.POST.get("otp_confirm"))

        try:
            truth = ContactNumberOTP.objects.get(
                contact_number=self.request.user.contact_number)
            print(f'{"-"*60}\nComparing{user_otp} and {truth.objects.otp}\n{"-"*60}')
            if user_otp == truth.objects.otp:
                request.user.contact_verified = True
                request.user.save()
                truth.delete()
        except ContactNumberOTP.DoesNotExist:
            pass
        finally:
            return redirect('contact')


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
