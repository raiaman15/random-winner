import os
import pyotp
import razorpay
from decimal import getcontext, ROUND_UP, Decimal
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, TemplateView, FormView
from allauth.account.admin import EmailAddress
from .models import CustomUser, ContactNumberOTP, BillingAddress, BankAccountDetail, BalanceTransaction, \
    InvestmentTransaction, SupportTicket
from .forms import (ProfileIdentityProofUploadViewForm, ProfilePictureViewForm, AccountResetPasswordWithOTPViewForm,
                    AccountResetPasswordWithOTPConfirmViewForm, ManagerProfileApprovePoolmasterViewForm)
from config.validators import validate_username
from pools.models import PoolInvite


##############################################################################
# User Onboard & Management Views
##############################################################################

class UserStatusView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        # User Group Based Redirect
        if user.groups.filter(name='manager').exists():
            return redirect('manager_profile_list')
        if user.groups.filter(name='master').exists():
            if PoolInvite.objects.filter(username=user.username).exists():
                return redirect('pool_invite_list')
            return redirect('pool_list')
        if user.groups.filter(name='member').exists():
            if PoolInvite.objects.filter(username=user.username).exists():
                return redirect('pool_invite_list')
            return redirect('pool_list')

        # If user signed up with email and confirmed their email address
        if EmailAddress.objects.filter(user=user).exists() and not user.contact_verified:
            if EmailAddress.objects.filter(user=user, verified=False).exists():
                return redirect('profile_verification_option')
            elif user.identity_reject_reason or not user.identity_proof:
                return redirect('profile_identity_proof_upload')
            elif not (user.first_name or user.last_name):
                return redirect('profile_name')
            else:
                return redirect('dashboard')

        # If user signed up with contact number (username in DB)
        if user.username:
            if not user.contact_verified:
                return redirect('profile_verification_sms')
            elif user.identity_reject_reason or not user.identity_proof:
                return redirect('profile_identity_proof_upload')
            elif not (user.first_name or user.last_name):
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
            return redirect('status')

        elif ContactNumberOTP.objects.filter(username=user.username).exists():
            td = timezone.now() - timedelta(minutes=5)
            attempts = ContactNumberOTP.objects.filter(username=self.request.user.username, created__gte=td)
            if len(attempts) > 2:
                messages.warning(request, '3+ OTP attempts in 5 minutes! Please try again in 5 minutes.')
            else:
                user.generate_otp()
                messages.success(
                    request, f'Please verify the OTP sent to your registered contact number {user.username}!')
        else:
            user.generate_otp()
            messages.success(request, f'Please verify the OTP sent to your registered contact number {user.username}!')

        return super(ProfileVerificationSMSView, self).get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request):
        user = request.user
        if user.contact_verified:
            messages.success(request, response_messages['profile_sms_verification_already_verified'])
            return redirect('status')

        if ContactNumberOTP.objects.filter(username=self.request.user.username).exists():
            user_otp = None
            if isinstance(request.POST.get("otp_confirm"), str):
                if len(request.POST.get("otp_confirm")) == 6:
                    user_otp = int(request.POST.get("otp_confirm"))

            totp = pyotp.TOTP(user.contact_secret)
            token_valid = totp.verify(str(user_otp), valid_window=3)
            if token_valid:
                request.user.contact_verified = True
                request.user.save()
                messages.success(request, response_messages['profile_sms_verification_successful'])
                ContactNumberOTP.objects.filter(username=user.username).delete()
            else:
                messages.error(request, response_messages['profile_sms_verification_incorrect_otp'])
                return redirect('profile_verification_sms')
        return redirect('status')


class ProfileIdentityProofUploadView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileIdentityProofUploadViewForm
    context_object_name = 'user'
    template_name = 'account/profile_identity_proof_upload.html'
    login_url = 'account_login'

    def get_object(self, queryset=None):
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
        messages.success(self.request, response_messages['profile_identity_proof_upload_successful'])
        return reverse_lazy('profile_name')


class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/dashboard.html'
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.identity_verified:
            messages.error(self.request, response_messages['profile_identity_proof_under_review'])

        return super(ProfileDashboardView, self).get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class ProfileNameView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name']
    context_object_name = 'user'
    template_name = 'account/profile_name.html'
    login_url = 'account_login'
    success_url = reverse_lazy('status')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class ProfileDetailView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'aadhaar_number', 'pan_number']
    context_object_name = 'user'
    template_name = 'account/profile_detail.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile_detail')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, response_messages['profile_detail_update_successful'])

        return super(ProfileDetailView, self).post(request, *args, **kwargs)


class ProfilePictureView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfilePictureViewForm
    context_object_name = 'user'
    template_name = 'account/profile_picture.html'
    login_url = 'account_login'
    success_url = reverse_lazy('profile_picture')

    def get_object(self, queryset=None):
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

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.first_name or user.last_name:
            if user.identity_verified:
                if user.aadhaar_number or user.pan_number:
                    if user.contact_verified:
                        if request.POST.get('is_willing_master') == 'on':
                            messages.success(self.request, response_messages['profile_apply_poolmaster_successful'])
                            return super(ProfileApplyPoolmasterView, self).post(request, *args, **kwargs)
                    else:
                        messages.error(self.request, response_messages['profile_contact_number_unverified'])
                        return redirect('profile_verification_sms')
                else:
                    messages.error(self.request, response_messages['profile_details_incomplete'])
                    return redirect('profile_detail')
            else:
                messages.error(self.request, response_messages['profile_identity_proof_unverified'])
                return redirect('profile_identity_proof_upload')
        else:
            messages.error(self.request, response_messages['profile_details_incomplete'])
            return redirect('profile_name')
        return redirect('status')


##############################################################################
# Password Reset Using SMS - OTP (account_reset_password_with_otp)
##############################################################################

class AccountResetPasswordWithOTPView(FormView):
    # username = None
    template_name = 'account/password_reset_with_otp.html'
    form_class = AccountResetPasswordWithOTPViewForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = None

    def post(self, request, *args, **kwargs):
        validate_username(request.POST.get("username"))
        self.username = int(request.POST.get("username"))
        if not CustomUser.objects.filter(username=self.username).exists():
            messages.error(
                request,
                f'There is no user registered with the provided contact number {self.username}. You can Sign Up if you are new user.')
        else:
            if ContactNumberOTP.objects.filter(username=self.username).exists():
                td = timezone.now() - timedelta(minutes=5)
                attempts = ContactNumberOTP.objects.filter(
                    username=self.username, created__gte=td)
                if len(attempts) > 2:
                    messages.warning(request, response_messages['profile_password_reset_attempt_exceeded'])
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
        if self.request.session['username'] == self.username:
            return reverse_lazy('account_reset_password_with_otp_confirm')
        return reverse_lazy('account_reset_password_with_otp')


class AccountResetPasswordWithOTPConfirmView(FormView):
    # username = None
    template_name = 'account/password_reset_with_otp_confirm.html'
    form_class = AccountResetPasswordWithOTPConfirmViewForm
    success_url = reverse_lazy('status')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = None

    def get(self, request, *args, **kwargs):
        attempt = int(request.session['password_reset_attempt']) + 1
        request.session['password_reset_attempt'] = attempt + 1
        if attempt > 2:
            messages.error(request, response_messages['profile_password_reset_attempt_exceeded'])
            return redirect('status')
        self.username = request.session['username']
        return super(AccountResetPasswordWithOTPConfirmView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.username = request.session['username']
        user_otp = None
        if isinstance(request.POST.get("otp"), str):
            if len(request.POST.get("otp")) == 6:
                user_otp = int(request.POST.get("otp"))
        contact_secret = get_object_or_404(CustomUser, username=self.username).contact_secret
        totp = pyotp.TOTP(contact_secret)
        token_valid = totp.verify(user_otp, valid_window=3)
        if token_valid:
            ContactNumberOTP.objects.filter(username=self.username).delete()
            request.session.flush()
            user = CustomUser.objects.get(username=self.username)
            user.set_password(f'{self.username}{user_otp}')
            user.save()
            messages.success(
                request,
                f'Password Changed! New password is {self.username}XXXXXX where XXXXXX is the OTP you just confirmed.')

        else:
            messages.error(
                request, response_messages['profile_password_reset_incorrect_otp'])
            return redirect('profile_verification_sms')
        return super(AccountResetPasswordWithOTPConfirmView, self).post(request, *args, **kwargs)


##############################################################################
# User Billing Address & Transactions Specific Views
##############################################################################

class ProfileBillingAddressCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = BillingAddress
    template_name = 'account/profile_billing_address.html'
    fields = ['name', 'address1', 'address2', 'zip_code', 'city', 'state', 'country']
    group_required = u"member"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileBillingAddressCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_billing_address_update', kwargs={'pk': self.request.user.id})


class ProfileBillingAddresssUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = BillingAddress
    template_name = 'account/profile_billing_address.html'
    fields = ['name', 'address1', 'address2', 'zip_code', 'city', 'state', 'country']
    group_required = u"member"

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, user_id=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileBillingAddresssUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_billing_address_update', kwargs={'pk': self.request.user.id})


class ProfileBankAccountDetailCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = BankAccountDetail
    template_name = 'account/profile_bank_account_detail.html'
    fields = ['bank_name', 'account_number', 'ifsc_code']
    group_required = u"member"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileBankAccountDetailCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_bank_account_detail_update', kwargs={'pk': self.request.user.id})


class ProfileBankAccountDetailUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = BankAccountDetail
    template_name = 'account/profile_bank_account_detail.html'
    fields = ['bank_name', 'account_number', 'ifsc_code']
    group_required = u"member"

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, user_id=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileBankAccountDetailUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_bank_account_detail_update', kwargs={'pk': self.request.user.id})


class ProfileBalanceTransactionListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = BalanceTransaction
    context_object_name = 'transactions'
    template_name = 'account/profile_balance_transaction_list.html'
    paginate_by = 100
    group_required = u"member"

    def get_queryset(self):
        user = self.request.user
        user.refresh_balance_investment()
        return self.model.objects.filter(user=user).order_by("-created")


class ProfileInvestmentTransactionListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = InvestmentTransaction
    context_object_name = 'transactions'
    template_name = 'account/profile_investment_transaction_list.html'
    paginate_by = 100
    group_required = u"member"

    def get_queryset(self):
        user = self.request.user
        user.refresh_balance_investment()
        return self.model.objects.filter(user=user).order_by("-created")


##############################################################################
# Payment Specific Views (Add Balance)
##############################################################################

class ProfileCreditBalanceView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = BalanceTransaction
    template_name = 'account/profile_balance_transaction_create.html'
    fields = ['amount', ]
    login_url = 'account_login'
    group_required = u"member"

    def form_valid(self, form):
        form.instance.type_of_transaction = 'C'
        form.instance.user = self.request.user
        getcontext().prec = 3
        getcontext().rounding = ROUND_UP
        form.instance.amount = abs(form.instance.amount)
        form.instance.tax = abs(Decimal(0.18) * form.instance.amount)  # Adding 18% GST
        # Initiate RazorPay Transaction
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        order_status = None
        try:
            response = client.order.create(
                dict(amount=round((form.instance.amount + form.instance.tax) * 100), currency='INR')
            )  # RazorPay Transactions are in Paise; Added GST
            order_id = response['id']
            order_status = response['status']
        except Exception as e:
            messages.error(self.request, f'Error Occurred: {e}')
            return redirect('profile_balance_credit_transaction_create')
        # Saving order_id in DB
        if order_status == 'created':
            form.instance.order_id = order_id
            return super(ProfileCreditBalanceView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_balance_transaction_confirm', kwargs={'pk': self.object.id})


class ProfileCreditBalanceConfirmView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = BalanceTransaction
    context_object_name = 'transaction'
    template_name = 'account/profile_balance_transaction_confirm.html'
    login_url = 'account_login'
    group_required = u"member"

    def get(self, request, *args, **kwargs):
        balance_transaction_id = self.kwargs['pk']
        balance_transaction = get_object_or_404(BalanceTransaction, id=balance_transaction_id)
        if balance_transaction in request.user.balance_transaction.all():
            return super(ProfileCreditBalanceConfirmView, self).get(request, *args, **kwargs)
        else:
            messages.error(self.request, 'Order ID Mismatch Error. Please try again!')
            return redirect('profile_balance_credit_transaction_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.RAZORPAY_KEY_ID
        return context


class ProfileCreditBalanceStatusView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = BalanceTransaction
    context_object_name = 'transaction'
    template_name = 'account/profile_balance_transaction_status.html'
    login_url = 'account_login'
    group_required = u"member"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileCreditBalanceStatusView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.error(request, 'Invalid Request')
        return redirect('status')

    def post(self, request, *args, **kwargs):
        balance_transaction_id = self.kwargs['pk']
        balance_transaction = get_object_or_404(BalanceTransaction, id=balance_transaction_id)

        if balance_transaction in request.user.balance_transaction.all() and balance_transaction.order_id == request.POST.get(
                'razorpay_order_id'):
            param_dict = {
                'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                'razorpay_order_id': balance_transaction.order_id,
                'razorpay_signature': request.POST.get('razorpay_signature')
            }

            # Verifying Signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

            try:
                client.utility.verify_payment_signature(param_dict)
                # Explicitly Reconfirm Payment Status at RazorPay Server
                payments = client.order.payments(request.POST.get('razorpay_order_id'))

                for payment in payments['items']:
                    if payment['id'] == request.POST.get('razorpay_payment_id'):
                        if payment['order_id'] == request.POST.get('razorpay_order_id'):
                            balance_transaction.make_verified(
                                request.POST.get('razorpay_payment_id'),
                                request.POST.get('razorpay_order_id'),
                                request.POST.get('razorpay_signature')
                            )
                            messages.success(
                                request, f'Payment Successful! ₹ {balance_transaction.amount} added to your balance.')

            except Exception as e:
                messages.error(request, f'Payment Failed: {e}')
                return redirect('profile_balance_transaction_list')
            return super(ProfileCreditBalanceStatusView, self).get(request, *args, **kwargs)
        else:
            messages.error(self.request, 'Order ID Mismatch Error. Please try again!')
            return redirect('profile_balance_transaction_status')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileDebitBalanceView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = BalanceTransaction
    template_name = 'account/profile_balance_transaction_create.html'
    fields = ['amount', ]
    login_url = 'account_login'
    group_required = u"member"

    def form_valid(self, form):
        form.instance.type_of_transaction = 'D'
        form.instance.user = self.request.user
        getcontext().prec = 3
        getcontext().rounding = ROUND_UP
        form.instance.amount = abs(form.instance.amount)
        form.instance.tax = abs(Decimal(0.0) * form.instance.amount)  # Adding 0% Processing Fee
        self.request.user.refresh_balance_investment()
        if form.instance.amount <= self.request.user.balance_amount:
            if self.request.user.billing_address and self.request.user.bank_account_detail:
                # Initiate Withdrawal Transaction
                prefix = self.request.user.username
                t = timezone.now()
                yy = t.strftime("%Y")
                mm = t.strftime("%m")
                dd = t.strftime("%d")
                hh = t.strftime("%H")
                # A Member can create only 1 withdrawal request per hour
                # mm = t.strftime("%M")

                form.instance.order_id = 'DEBIT' + prefix + yy + mm + dd + hh  # +mm
                try:
                    return super(ProfileDebitBalanceView, self).form_valid(form)
                except Exception as e:
                    messages.error(self.request, f'Error Occurred: {e}')
                    return redirect('profile_balance_debit_transaction_create')
            else:
                messages.error(self.request, response_messages['profile_bank_account_detail_incomplete'])
                return redirect('profile_bank_account_detail_create')
        else:
            messages.error(self.request, response_messages['profile_account_balance_low'])
            return redirect('profile_balance_debit_transaction_create')

    def get_success_url(self):
        return reverse_lazy('profile_balance_transaction_list')


##############################################################################
# Support Ticket Specific Views
##############################################################################


class ProfileSupportTicketCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = SupportTicket
    template_name = 'account/profile_support_ticket_create.html'
    fields = ['type_of_ticket', 'user_message', 'closed']
    login_url = 'account_login'
    group_required = u"member"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileSupportTicketCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_support_ticket_list')


class ProfileSupportTicketUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = SupportTicket
    context_object_name = 'ticket'
    template_name = 'account/profile_support_ticket_update.html'
    fields = ['closed', ]
    login_url = 'account_login'
    group_required = u"member"

    def form_valid(self, form):
        if form.instance.user == self.request.user:
            return super(ProfileSupportTicketUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_support_ticket_update', kwargs={'pk': self.kwargs['pk']})


class ProfileSupportTicketListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = SupportTicket
    context_object_name = 'tickets'
    template_name = 'account/profile_support_ticket_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"member"

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user).order_by("closed", "-created")


##############################################################################
# Manager Specific Views (User & Action Management)
##############################################################################


class ManagerProfileListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'profiles'
    template_name = 'account/manager_profile_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        return self.model.objects.filter(~Q(groups__name='manager') & Q(is_superuser=False)).order_by("username")


class ManagerProfileListPoolMemberView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'profiles'
    template_name = 'account/manager_profile_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        return self.model.objects.filter(Q(groups__name='member')).order_by("username")


class ManagerProfileListPoolMasterView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'profiles'
    template_name = 'account/manager_profile_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        return self.model.objects.filter(Q(groups__name='master')).order_by("username")


class ManagerProfileListWillingPoolMasterView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'profiles'
    template_name = 'account/manager_profile_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        return self.model.objects.filter(
            ~Q(groups__name='master') & Q(groups__name='member') & Q(is_willing_master=True)).order_by("username")


class ManagerProfileListUnverifiedProfileView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'profiles'
    template_name = 'account/manager_profile_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        return self.model.objects.filter(
            ~Q(groups__name='manager') & Q(is_superuser=False) & Q(identity_verified=False)).order_by("username")


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
        form.instance.master = get_object_or_404(
            self.model, pk=self.kwargs['pk'])
        if bool(form.cleaned_data['identity_verified']):
            user = get_object_or_404(self.model, pk=self.kwargs['pk'])
            # Managers are not allowed to become Members
            if not user.groups.filter(name='manager').exists():
                master_group = Group.objects.get(name='member')
                master_group.user_set.add(user)
                messages.success(
                    self.request, f'{user.username} is now a PoolMember.')

        return super(ManagerProfileVerifyIdentityView, self).form_valid(form)


class ManagerProfileApprovePoolmasterView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    # profile = None
    template_name = 'account/manager_profile_approve_poolmaster.html'
    form_class = ManagerProfileApprovePoolmasterViewForm
    group_required = u"manager"

    def __init__(self):
        super().__init__()
        self.profile = None

    def get(self, request, *args, **kwargs):
        self.profile = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return super(ManagerProfileApprovePoolmasterView, self).get(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        if bool(form.cleaned_data['confirm']):
            user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
            # Managers are not allowed to become Members
            if not user.groups.filter(name='manager').exists():
                master_group = Group.objects.get(name='master')
                master_group.user_set.add(user)
                messages.success(
                    self.request, f'{user.username} is now a PoolMaster.')
        return super(ManagerProfileApprovePoolmasterView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('manager_profile_detail', kwargs={'pk': self.kwargs['pk']})


class ManagerProfileSearchView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'profile_list'
    template_name = 'account/manager_profile_list.html'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.objects.filter(
            Q(email__icontains=query) | Q(first_name__icontains=query) |
            Q(last_name__icontains=query) | Q(username__icontains=query)
        ).order_by("username")


class ManagerFinancialSupportTicketListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = SupportTicket
    context_object_name = 'tickets'
    template_name = 'account/manager_support_ticket_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        return self.model.objects.filter(Q(type_of_ticket='F')).order_by("closed", "-created")


class ManagerApplicationSupportTicketListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = SupportTicket
    context_object_name = 'tickets'
    template_name = 'account/manager_support_ticket_list.html'
    login_url = 'account_login'
    paginate_by = 100
    group_required = u"manager"

    def get_queryset(self):
        return self.model.objects.filter(Q(type_of_ticket='A')).order_by("closed", "-created")


class ManagerSupportTicketUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = SupportTicket
    context_object_name = 'ticket'
    template_name = 'account/manager_support_ticket_update.html'
    fields = ['manager_message', 'closed']
    login_url = 'account_login'
    group_required = u"manager"

    def get_success_url(self):
        return reverse_lazy('manager_support_ticket_update', kwargs={'pk': self.kwargs['pk']})


class ManagerManagePoolView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = InvestmentTransaction
    context_object_name = 'payments'
    paginate_by = 100
    template_name = 'account/manager_pool_manage.html'
    login_url = 'account_login'
    group_required = u"manager"

    def get_queryset(self):
        now = timezone.now()
        yy = now.year
        mm = now.month
        return self.model.objects.filter(created__year=yy, created__month=mm, type_of_transaction='D').all()
