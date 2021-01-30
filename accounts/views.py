from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from datetime import datetime
import pytz
from PIL import Image
from django.db.models import Q
from django.views.generic import View, ListView, DetailView, UpdateView, TemplateView
from .models import CustomUser, ContactNumberOTP
from .forms import CustomUserProfileUpdateForm
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('user_permission.user_edit'):
            raise PermissionDenied
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/user_detail.html'
    login_url = 'account_login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('user_permission.user_edit'):
            raise PermissionDenied
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)


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
    success_url = reverse_lazy('contact_confirm')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class UserContactConfirmView(LoginRequiredMixin, TemplateView):
    message = ''
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/contact_confirm.html'
    login_url = 'account_login'
    success_url = reverse_lazy('contact_confirm')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.contact_verified:
            self.message = "You have already verified your contact number!"
        elif ContactNumberOTP.objects.filter(contact_number=user.contact_number).exists():
            attempt = ContactNumberOTP.objects.get(
                contact_number=user.contact_number)
            now = pytz.timezone("Asia/Kolkata").localize(datetime.now())
            print((now-attempt.created_at).total_seconds()//60)
            if (now-attempt.created_at).total_seconds()//60 < 5:
                self.message = "You requested OTP within past 5 minutes. Please try again later!"
            else:
                ContactNumberOTP.objects.get(
                    contact_number=user.contact_number).delete()
                user.generate_otp()
        else:
            user.generate_otp()

        return super(UserContactConfirmView, self).get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(UserContactConfirmView,
                        self).get_context_data(**kwargs)
        context['message'] = self.message
        return context

    def post(self, request):
        if request.user.contact_verified:
            return redirect('contact')

        if ContactNumberOTP.objects.filter(contact_number=self.request.user.contact_number).exists():

            user_otp = 0
            if isinstance(request.POST.get("otp_confirm"), str):
                if len(request.POST.get("otp_confirm")) == 6:
                    user_otp = int(request.POST.get("otp_confirm"))
            truth = ContactNumberOTP.objects.get(
                contact_number=self.request.user.contact_number)
            print(f'{"-"*60}\nComparing {user_otp} and {truth.otp}\n{"-"*60}')
            if int(user_otp) == int(truth.otp):
                request.user.contact_verified = True
                request.user.save()
                truth.delete()

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
