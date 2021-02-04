import os
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, TemplateView, FormView
from allauth.account.admin import EmailAddress
from .models import CustomUser, ContactNumberOTP
from .forms import (ProfileIdentityProofUploadViewForm, ProfilePictureViewForm, AccountResetPasswordWithOTPViewForm,
                    AccountResetPasswordWithOTPConfirmViewForm, ManagerProfileApprovePoolmasterViewForm)
from config.validators import validate_username


class UserStatusView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        # If user signed up with email and confirmed their email address
        if (EmailAddress.objects.filter(user=user).exists() and not user.contact_verified):
            if (EmailAddress.objects.filter(user=user, verified=False).exists()):
                return redirect('profile_verification_option')
            elif user.identity_reject_reason or not user.identity_proof:
                return redirect('profile_identity_proof_upload')
            elif not (user.first_name or user.lastname):
                return redirect('profile_name')
            else:
                return redirect('dashboard')

        # If user signed up with contact number (username in DB)
        if user.username:
            if not user.contact_verified:
                return redirect('profile_verification_sms')
            elif user.identity_reject_reason or not user.identity_proof:
                return redirect('profile_identity_proof_upload')
            elif not (user.first_name or user.lastname):
                return redirect('profile_name')
            else:
                return redirect('dashboard')


class ProfileVerificationOptionView(TemplateView):
    template_name = 'account/profile_verification_option.html'


class ProfileVerificationSMSView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/profile_verification_sms.html'
    login_url = 'account_login'
    success_url = reverse_lazy('status')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.contact_verified:
            messages.success(request, 'You have already verified!')
        elif ContactNumberOTP.objects.filter(username=user.username).exists():
            td = timezone.now() - timedelta(minutes=5)
            attempts = ContactNumberOTP.objects.filter(
                username=self.request.user.username, created__gte=td)
            if len(attempts) > 2:
                messages.warning(
                    request, 'More than 3 OTP requests are not allowed within 5 minutes. Please type the last OTP or try again in 5 minutes for new OTP!')
            else:
                user.generate_otp()
        else:
            user.generate_otp()
        return super(ProfileVerificationSMSView, self).get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request):
        user = request.user
        if user.contact_verified:
            return redirect('status')
        if ContactNumberOTP.objects.filter(username=self.request.user.username).exists():
            user_otp = None
            if isinstance(request.POST.get("otp_confirm"), str):
                if len(request.POST.get("otp_confirm")) == 6:
                    user_otp = int(request.POST.get("otp_confirm"))
            truth = ContactNumberOTP.objects.filter(
                username=user.username).last()
            if int(user_otp) == int(truth.otp):
                request.user.contact_verified = True
                request.user.save()
                messages.success(request, 'Contact Number Verified')
                ContactNumberOTP.objects.filter(
                    username=user.username).delete()
            else:
                messages.error(
                    request, 'Incorrect OPT. Please type correct OTP or try again in 5 minutes.')
                return redirect('profile_verification_sms')
        return redirect('status')


class ProfileIdentityProofUploadView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileIdentityProofUploadViewForm
    context_object_name = 'user'
    template_name = 'account/profile_identity_proof_upload.html'
    login_url = 'account_login'

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        if request.FILES:
            if request.FILES['identity_proof'].size > 2048000:
                return HttpResponse('File size exceeded specified limit!')
            else:
                if request.user.identity_proof:
                    os.remove(request.user.identity_proof.path)
                    request.user.identity_proof = None
                    request.user.save()
        return super(ProfileIdentityProofUploadView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(
            self.request, 'Identity Proof Uploaded Successfully! Our Team will verify it soon.')
        return reverse_lazy('profile_name')


class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/dashboard.html'
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.identity_verified:
            messages.error(
                self.request, 'Identity Proof Not Verified! You won\'t be able to perform any operation until verification.')

        return super(ProfileDashboardView, self).get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class ProfileNameView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name']
    context_object_name = 'user'
    template_name = 'account/profile_name.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile_name')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class ProfileDetailView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'aadhaar_number', 'pan_number']
    context_object_name = 'user'
    template_name = 'account/profile_detail.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile_detail')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        messages.success(
            self.request, 'Details Updated Successfully.')

        return super(ProfileDetailView, self).post(request, *args, **kwargs)


class ProfilePictureView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfilePictureViewForm
    context_object_name = 'user'
    template_name = 'account/profile_picture.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile_picture')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        if request.FILES:
            if request.FILES['picture'].size > 2048000:
                return HttpResponse('File size exceeded specified limit!')
            else:
                if request.user.picture:
                    os.remove(request.user.picture.path)
                    request.user.picture = None
                    request.user.save()

        return super(ProfilePictureView, self).post(request, *args, **kwargs)


class ProfileApplyPoolmasterView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['is_willing_master']
    context_object_name = 'user'
    template_name = 'account/profile_apply_poolmaster.html'
    login_url = 'account_login'
    success_url = reverse_lazy('status')
    group_required = u"member"

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        if request.POST.get('is_willing_master') == 'on':
            messages.success(
                self.request, 'Successfully Applied for PoolMaster. Our Team will reach out to you soon.')

        return super(ProfileApplyPoolmasterView, self).post(request, *args, **kwargs)


##############################################################################
# Password Reset Using SMS - OTP (account_reset_password_with_otp)
##############################################################################
class AccountResetPasswordWithOTPView(FormView):
    username = None
    template_name = 'account/password_reset_with_otp.html'
    form_class = AccountResetPasswordWithOTPViewForm

    def post(self, request, *args, **kwargs):
        validate_username(request.POST.get("username"))
        self.username = int(request.POST.get("username"))
        if not CustomUser.objects.filter(username=self.username).exists():
            messages.error(
                request, f'There is no user registered with the provided contact number {self.username}. You can Sign Up if you are new user.')
        else:
            if ContactNumberOTP.objects.filter(username=self.username).exists():
                td = timezone.now() - timedelta(minutes=5)
                attempts = ContactNumberOTP.objects.filter(
                    username=self.username, created__gte=td)
                if len(attempts) > 2:
                    messages.warning(
                        request, 'More than 3 OTP requests are not allowed within 5 minutes. Please type the last OTP or try again in 5 minutes for new OTP!')
                else:
                    request.session['username'] = self.username
                    request.session['password_reset_attempt'] = 0
                    CustomUser.objects.get(
                        username=self.username).generate_otp()
                    messages.success(
                        request, f'Please verify the OTP sent to your registered contact number {self.username}.')
            else:
                request.session['username'] = self.username
                request.session['password_reset_attempt'] = 0
                CustomUser.objects.get(username=self.username).generate_otp()
                messages.success(
                    request, f'Please verify the OTP sent to your registered contact number {self.username}.')
        return super(AccountResetPasswordWithOTPView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('account_reset_password_with_otp_confirm')


class AccountResetPasswordWithOTPConfirmView(FormView):
    username = None
    template_name = 'account/password_reset_with_otp_confirm.html'
    form_class = AccountResetPasswordWithOTPConfirmViewForm
    success_url = reverse_lazy('status')

    def get(self, request, *args, **kwargs):
        attempt = int(request.session['password_reset_attempt'])+1
        request.session['password_reset_attempt'] = attempt+1
        if attempt > 2:
            messages.error(
                request, 'Too many attempts. Please try again later!')
            return redirect('status')
        self.username = request.session['username']
        return super(AccountResetPasswordWithOTPConfirmView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.username = request.session['username']
        user_otp = None
        if isinstance(request.POST.get("otp"), str):
            if len(request.POST.get("otp")) == 6:
                user_otp = int(request.POST.get("otp"))
        truth = ContactNumberOTP.objects.filter(username=self.username).last()
        if int(user_otp) == int(truth.otp):
            ContactNumberOTP.objects.filter(username=self.username).delete()
            request.session.flush()
            user = CustomUser.objects.get(username=self.username)
            user.set_password(f'{self.username}{user_otp}')
            user.save()
            messages.success(
                request, f'Password Changed. New password is {self.username}XXXXXX where XXXXXX is the OTP you just confirmed.')

        else:
            messages.error(
                request, 'Incorrect OPT. Please type correct OTP or try again in 5 minutes.')
            return redirect('profile_verification_sms')
        return super(AccountResetPasswordWithOTPConfirmView, self).post(request, *args, **kwargs)

##############################################################################
# Manager Specific Views
##############################################################################


class ManagerProfileListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'profiles'
    template_name = 'account/manager_profile_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"manager"


class ManagerProfileDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'profile'
    template_name = 'account/manager_profile_detail.html'
    login_url = 'account_login'
    group_required = u"manager"


class ManagerProfileVerifyIdentityView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = CustomUser
    context_object_name = 'profile'
    template_name = 'account/manager_profile_verify_identity.html'
    fields = ['identity_verified', 'identity_reject_reason']
    group_required = u"manager"

    def form_valid(self, form):
        form.instance.master = self.request.user
        # if request.POST.get('is_willing_master') == 'on':
        return super(ManagerProfileVerifyIdentityView, self).form_valid(form)


class ManagerProfileApprovePoolmasterView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    context_object_name = 'profile'
    template_name = 'account/manager_profile_approve_poolmaster.html'
    form_class = ManagerProfileApprovePoolmasterViewForm
    group_required = u"manager"

    def form_valid(self, form, *args, **kwargs):
        if form.confirm == 'on':
            user = CustomUser.objects.get(id=self.kwargs['pk'])
            user.groups.add('master')
            user.save()
            messages.success(
                self.request, f'{user.username} is now a PoolMaster.')
        return super(ManagerProfileApprovePoolmasterView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('manager_profile_detail',  kwargs={'pk': self.kwargs['pk']})


class ManagerProfileSearchView(ListView, GroupRequiredMixin):
    model = CustomUser
    context_object_name = 'profile_list'
    template_name = 'account/profile_list.html'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.objects.filter(
            Q(email__icontains=query) | Q(first_name__icontains=query) |
            Q(last_name__icontains=query) | Q(username__icontains=query)
        )
