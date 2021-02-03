import os
import pytz
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from braces.views import GroupRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, TemplateView
from allauth.account.admin import EmailAddress
from .models import CustomUser, ContactNumberOTP
from .forms import ProfileIdentityProofUploadViewForm, ProfilePictureViewForm


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
            messages.success(
                request, 'You have already verified your contact number!')
        elif ContactNumberOTP.objects.filter(username=user.username).exists():
            attempt = ContactNumberOTP.objects.get(
                username=user.username).created_at
            now = pytz.timezone("Asia/Kolkata").localize(datetime.now())
            if (now-attempt).total_seconds()//60 < 5:
                messages.warning(
                    request, 'You requested OTP within past 5 minutes. Please type the same OTP or try again in 5 minutes for new OTP!')
            else:
                ContactNumberOTP.objects.get(username=user.username).delete()
                user.generate_otp()
        else:
            user.generate_otp()

        return super(ProfileVerificationSMSView, self).get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileVerificationSMSView,
                        self).get_context_data(**kwargs)
        return context

    def post(self, request):
        if request.user.contact_verified:
            return redirect('status')

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
    template_name = 'account/poolmaster_apply.html'
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
# from django.contrib.auth.models import User
# u = User.objects.get(username__exact='john')
# u.set_password('new password')
# u.save()
##############################################################################
class AccountResetPasswordWithOTPView(TemplateView):
    template_name = 'account/password_reset_with_otp.html'

##############################################################################
# Manager Specific Views
##############################################################################


class ManagerProfileListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'profile_list'
    template_name = 'account/profile_list.html'
    login_url = 'account_login'
    paginate_by = 200
    group_required = u"manager"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('user_permission.user_edit'):
            raise PermissionDenied
        return super(ManagerProfileListView, self).dispatch(request, *args, **kwargs)


class ManagerProfileDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/profile_detail.html'
    login_url = 'account_login'
    group_required = u"manager"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('user_permission.user_edit'):
            raise PermissionDenied
        return super(ManagerProfileDetailView, self).dispatch(request, *args, **kwargs)


class ManagerVerifyProfileIdentityView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    selected_user_id = None
    model = CustomUser
    template_name = 'account/profile_verify_identity.html'
    fields = ['identity_verified', 'identity_reject_reason']
    group_required = u"manager"

    def form_valid(self, form):
        form.instance.master = self.request.user
        return super(ManagerVerifyProfileIdentityView, self).form_valid(form)


class ManagerProfileSearchView(ListView, GroupRequiredMixin):
    model = CustomUser
    context_object_name = 'profile_list'
    template_name = 'account/profile_list.html'
    paginate_by = 200
    group_required = u"manager"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.objects.filter(
            Q(email__icontains=query) | Q(first_name__icontains=query) |
            Q(last_name__icontains=query) | Q(username__icontains=query)
        )
