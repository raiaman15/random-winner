import os
import pytz
from datetime import datetime
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, TemplateView

from allauth.account.admin import EmailAddress

from .models import CustomUser, ContactNumberOTP
from .forms import UserIdentityProofUploadViewForm, UserProfilePictureUploadViewForm


class UserStatusView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        # If user signed up with email and confirmed their email address
        if (EmailAddress.objects.filter(user=user).exists() and not user.contact_verified):
            if (EmailAddress.objects.filter(user=user, verified=False).exists()):
                return redirect('contact_confirmation_option')
            elif user.identity_reject_reason or not user.identity_proof:
                return redirect('identity_proof_upload')
            elif not (user.first_name or user.lastname):
                return redirect('profile_name')
            else:
                return redirect('dashboard')

        # If user signed up with contact number
        if user.username:
            if not user.contact_verified:
                return redirect('contact_sms_confirm')
            elif user.identity_reject_reason or not user.identity_proof:
                return redirect('identity_proof_upload')
            elif not (user.first_name or user.lastname):
                return redirect('profile_name')
            else:
                return redirect('dashboard')


class UserContactConfirmOptionView(TemplateView):
    template_name = 'account/contact_confirmation_option.html'


class UserContactSMSConfirmView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/contact_sms_confirm.html'
    login_url = 'account_login'
    success_url = reverse_lazy('status')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.contact_verified:
            # self.message = "You have already verified your contact number!"
            messages.success(
                request, 'You have already verified your contact number!')
        elif ContactNumberOTP.objects.filter(username=user.username).exists():
            attempt = ContactNumberOTP.objects.get(
                username=user.username)
            now = pytz.timezone("Asia/Kolkata").localize(datetime.now())
            print((now-attempt.created_at).total_seconds()//60)
            if (now-attempt.created_at).total_seconds()//60 < 5:
                # self.message = "You requested OTP within past 5 minutes. Please try again later!"
                messages.warning(
                    request, 'You requested OTP within past 5 minutes. Please try again later!')
            else:
                ContactNumberOTP.objects.get(
                    username=user.username).delete()
                user.generate_otp()
        else:
            user.generate_otp()

        return super(UserContactSMSConfirmView, self).get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(UserContactSMSConfirmView,
                        self).get_context_data(**kwargs)
        return context

    def post(self, request):
        if request.user.contact_verified:
            return redirect('contact')

        if ContactNumberOTP.objects.filter(username=self.request.user.username).exists():

            user_otp = 0
            if isinstance(request.POST.get("otp_confirm"), str):
                if len(request.POST.get("otp_confirm")) == 6:
                    user_otp = int(request.POST.get("otp_confirm"))
            truth = ContactNumberOTP.objects.get(
                username=self.request.user.username)
            if int(user_otp) == int(truth.otp):
                request.user.contact_verified = True
                request.user.save()
                truth.delete()
                messages.success(request, 'Contact Number Verified')
            else:
                messages.error(
                    request, 'Incorrect OPT. Please try again in some time.')
                return redirect('contact_sms_confirm')
        return redirect('status')


class UserIdentityProofUploadView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserIdentityProofUploadViewForm
    context_object_name = 'user'
    template_name = 'account/identity-proof-upload.html'
    login_url = 'account_login'

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        if request.FILES:
            if request.FILES['identity_proof'].size > 2048000:
                return HttpResponse('File size exceeded specified limit!')
            else:
                # Delete old image file from system
                if request.user.identity_proof:
                    os.remove(request.user.identity_proof.path)
                    request.user.identity_proof = None
                    request.user.save()
        return super(UserIdentityProofUploadView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(
            self.request, 'Identity Proof Uploaded Successfully! Our Team will verify it soon.')
        return reverse_lazy('profile_name')


class DashboardView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/dashboard.html'
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.identity_verified:
            messages.error(
                self.request, 'Identity Proof Not Verified! You won\'t be able to perform any operation until verification.')

        return super(DashboardView, self).get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class UserProfileNameUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name']
    context_object_name = 'user'
    template_name = 'account/profile-name.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile_name')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class UserProfileDetailUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'aadhaar_number', 'pan_number']
    context_object_name = 'user'
    template_name = 'account/profile-detail.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile_detail')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        messages.success(
            self.request, 'Details Updated Successfully.')

        return super(UserProfileDetailUpdateView, self).post(request, *args, **kwargs)


class UserProfilePictureUploadView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfilePictureUploadViewForm
    context_object_name = 'user'
    template_name = 'account/profile.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile_picture')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        if request.FILES:
            if request.FILES['picture'].size > 2048000:
                return HttpResponse('File size exceeded specified limit!')
            else:
                # Delete old image file from system
                if request.user.picture:
                    os.remove(request.user.picture.path)
                    request.user.picture = None
                    request.user.save()

        return super(UserProfilePictureUploadView, self).post(request, *args, **kwargs)


class UserPoolMasterApplicationView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['is_willing_master']
    context_object_name = 'user'
    template_name = 'account/poolmaster-apply.html'
    login_url = 'account_login'
    success_url = reverse_lazy('status')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.identity_verified:
            messages.error(
                self.request, 'Successfully Applied for PoolMaster. Our Team will reach out to you soon.')

        return super(UserPoolMasterApplicationView, self).post(request, *args, **kwargs)


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'account/user_list.html'
    login_url = 'account_login'
    paginate_by = 1

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


class SearchResultsListView(ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'account/user_list.html'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.objects.filter(
            Q(email__icontains=query) | Q(first_name__icontains=query) |
            Q(last_name__icontains=query) | Q(username__icontains=query)
        )
