import pyotp
import razorpay
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, DecimalValidator
from config.validators import (validate_name, validate_aadhaar_number, validate_pan_number, validate_username, validate_amount,
                               validate_balance_type_of_transaction, validate_investment_type_of_transaction, validate_support_ticket_type_of_ticket, validate_message)
from config.utils import send_otp
from django.db.models import Q
from decimal import Decimal


class CustomUser(AbstractUser):
    username = models.CharField(
        'Contact Number',
        max_length=12, blank=False, unique=True,
        validators=[validate_username],
        help_text='Your valid mobile number for OTP verification.'
    )
    first_name = models.CharField(
        'First Name',
        max_length=26, validators=[validate_name], blank=True,
        help_text='Your first name. (to be used in future transactions)'
    )
    last_name = models.CharField(
        'Last Name',
        max_length=26, validators=[validate_name], blank=True,
        help_text='Your last name. (to be used in future transactions)'
    )
    picture = models.ImageField(
        'Profile Picture',
        upload_to='picture/', blank=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        help_text='Your recent picture (must match with picture in photo ID below) in .png or .jpg format. (Max 2 MB)'
    )
    aadhaar_number = models.CharField(
        'Aadhaar Card Number',
        max_length=12, validators=[validate_aadhaar_number], blank=True,
        help_text='Your 12 digit Aadhaar Number (as written on your aadhaar card).'
    )
    pan_number = models.CharField(
        'PAN Card Number',
        max_length=10, validators=[validate_pan_number], blank=True,
        help_text='Your 10 digit PAN Number (as written on your PAN card).'
    )
    identity_proof = models.ImageField(
        'Identity Proof Photograph',
        upload_to='identity/', blank=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        help_text='Your photo ID proof (preferably Aadhaar Card) in .png or .jpg format. (Max 2 MB)'
    )
    identity_verified = models.BooleanField(default=False)
    identity_reject_reason = models.CharField(
        'ID Proof Rejection Reason',
        max_length=250, blank=True,
        help_text='The reason to Reject user\'s Identity Verification (by Internal Team).'
    )
    contact_secret = models.CharField(max_length=16, blank=True)
    contact_verified = models.BooleanField(default=False)
    is_willing_master = models.BooleanField(default=False)
    # Maximum Balance of 9,99,999 at given time
    balance_amount = models.DecimalField(
        'Balance Amount',
        default=0.00, max_digits=8, decimal_places=2,
        validators=[DecimalValidator, validate_amount]
    )
    # Maximum Transaction of 99,999 at given time
    investment_amount = models.DecimalField(
        'Investment Amount',
        default=0.00, max_digits=7, decimal_places=2,
        validators=[DecimalValidator, validate_amount]
    )

    def generate_otp(self):
        if not self.contact_secret:
            self.contact_secret = pyotp.random_base32()
            self.save()
        totp = pyotp.TOTP(self.contact_secret).now()
        send_otp(self.username, totp)
        ContactNumberOTP(username=self.username).save()

    def refresh_balance_investment(self):
        nba, nia = Decimal(0.00), Decimal(0.00)
        # Balance
        if BalanceTransaction.objects.filter(user=self, verified=True).exists():
            bts = BalanceTransaction.objects.filter(user=self, verified=True).all()
            btc = sum([t.amount for t in bts if t.type_of_transaction == 'C'])
            btd = sum([t.amount for t in bts if t.type_of_transaction == 'D'])
            # Net Balance Amount
            nba = btc-btd
        # Investment
        if InvestmentTransaction.objects.filter(user=self, verified=True).exists():
            its = InvestmentTransaction.objects.filter(user=self, verified=True).all()
            iti = sum([t.amount for t in its if t.type_of_transaction == 'I'])
            itd = sum([t.amount for t in its if t.type_of_transaction == 'D'])
            # Net Investment Amount
            nia = iti-itd
        # Net Final Balance & Investment
        self.balance_amount = nba-nia
        self.investment_amount = nia
        return super(CustomUser, self).save()

    def initiate_deposit(self, amount):
        # Refresh User's Balance
        self.refresh_balance_investment()
        # If they have sufficient balance
        if self.groups(name='member').exists():
            pass

    def initiate_withdrawal(self, amount):
        if self.groups(name='member').exists():
            pass
            # TODO-NORMAL: Raise request for admin.

    def get_absolute_url(self):
        return reverse('manager_profile_detail', args=[str(self.id)])

    def __str__(self):
        return self.username


class ContactNumberOTP(models.Model):
    username = models.CharField(
        max_length=12, blank=False,
        validators=[validate_username], editable=False
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)


class BalanceTransaction(models.Model):
    TRANSACTION_TYPE = (
        ('C', 'Credit'),
        ('D', 'Debit')

    )
    # Payment Gateway's Reference ID fro Credit otherwise System Generated
    order_id = models.CharField(max_length=250, blank=False)
    payment_id = models.CharField(max_length=250, blank=True)  # Payment Gateway's Payment ID
    payment_signature = models.CharField(max_length=250, blank=True)  # Payment Gateway's Signature
    user = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='balance_transaction', blank=False
    )
    type_of_transaction = models.CharField(
        max_length=1, choices=TRANSACTION_TYPE, blank=False,
        validators=[validate_balance_type_of_transaction]
    )
    amount = models.DecimalField(
        null=False, blank=False, max_digits=9, decimal_places=2,
        validators=[validate_amount],
        help_text="The amount in INR to be added (Taxes will be added on this amount)"
    )
    tax = models.DecimalField(
        null=False, blank=False, max_digits=9, decimal_places=2,
        validators=[validate_amount]
    )
    verified = models.BooleanField(default=False, editable=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self):
        self.full_clean()
        return super(BalanceTransaction, self).save()

    def make_verified(self, payment_id, order_id, payment_signature):
        if self.order_id == order_id:
            self.payment_id = payment_id
            self.payment_signature = payment_signature
            self.verified = True
            self.save()

    def __str__(self):
        return f'{self.user.username} : {self.type_of_transaction} : {self.created}'


class InvestmentTransaction(models.Model):
    TRANSACTION_TYPE = (
        ('I', 'Invest'),
        ('D', 'Disinvest')
    )
    type_of_transaction = models.CharField(
        max_length=1, choices=TRANSACTION_TYPE, blank=False,
        validators=[validate_investment_type_of_transaction]
    )
    amount = models.DecimalField(
        null=False, blank=False, max_digits=7, decimal_places=2,
        validators=[validate_amount]
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING,
                             related_name='outgoing_investment_transactions', blank=False)
    pool = models.ForeignKey('pools.Pool', on_delete=models.DO_NOTHING,
                             related_name='investment_transactions', blank=False)
    verified = models.BooleanField(default=False, editable=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self):
        self.full_clean()
        if self.verified == True:
            # TODO-NORMAL: Generate and send invoice
            pass
        return super(InvestmentTransaction, self).save()

    def __str__(self):
        return f'{self.user.username} : {self.type_of_transaction} : {self.pool.id} : {self.amount}'


class BillingAddress(models.Model):
    COUNTRY = (
        ('IN', 'India'),
    )
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING,
                                related_name='billing_address', blank=False)
    name = models.CharField("Full Name", max_length=64, validators=[validate_name], help_text="Name for Billing")
    address1 = models.CharField("Address Line 1", max_length=128, help_text="Line 1 of the Address")
    address2 = models.CharField("Address Line 2", max_length=128, help_text="Line 2 of the Address")
    zip_code = models.CharField("ZIP / Postal code", max_length=12, help_text="ZIP / Postal code for the Address")
    city = models.CharField("City", max_length=128, help_text="City for the Address")
    state = models.CharField("State", max_length=128, help_text="State for the Address")
    country = models.CharField("Country", max_length=3, choices=COUNTRY)

    def get_absolute_url(self):
        return reverse('profile_billing_address_update', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}, {self.address1}, {self.address2}'


class BankAccountDetail(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING,
                                related_name='bank_account_detail', blank=False)
    bank_name = models.CharField("Bank Name", max_length=64, validators=[validate_name], help_text="Name of Bank")
    account_number = models.CharField("Account Number", max_length=64, help_text="Your Account Number")
    ifsc_code = models.CharField("IFSC Code", max_length=64, help_text="Your IFSC Code")

    def get_absolute_url(self):
        return reverse('profile_bank_account_detail_update', args=[str(self.id)])

    def __str__(self):
        return f'{self.user.username} : {self.account_number}'


class SupportTicket(models.Model):
    TICKET_TYPE = (
        ('F', 'Finance Related'),
        ('A', 'Application Related')
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='support_ticket', blank=False)

    type_of_ticket = models.CharField(
        max_length=1, choices=TICKET_TYPE, blank=False,
        validators=[validate_support_ticket_type_of_ticket]
    )

    user_message = models.TextField(
        'Description of Issue',
        max_length=1000, validators=[validate_message], blank=True,
        help_text='Please elaborate the issues you are facing.'
    )

    manager_message = models.TextField(
        'Resolution Response',
        max_length=1000, validators=[validate_message], blank=True,
        help_text='Please elaborate the resolution of the issue.'
    )

    closed = models.BooleanField(default=False, editable=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def get_absolute_url(self):
        pass

    def __str__(self):
        pass
