import pyotp
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, DecimalValidator
from config.validators import (validate_name, validate_aadhaar_number, validate_pan_number, validate_username,
                               validate_amount, validate_otp, validate_balance_type_of_transaction, validate_investment_type_of_transaction)
from config.utils import send_otp


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
    balance_amount = models.DecimalField(
        'Balance Amount',
        default=0.00, max_digits=7, decimal_places=2,
        validators=[DecimalValidator, validate_amount]
    )
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
        # Balance
        bts = BalanceTransaction.objects.filter(user=self, verified=True).all()
        btc = [t.amount for t in bts if t.type_of_transaction == 'C']
        btd = [t.amount for t in bts if t.type_of_transaction == 'D']
        # Net Balance Amount
        nba = btc-btd
        # Investment
        its = InvestmentTransaction.objects.filter(
            user=self, verified=True).all()
        iti = [t.amount for t in its if t.type_of_transaction == 'I']
        itd = [t.amount for t in its if t.type_of_transaction == 'D']
        # Net Investment Amount
        nia = iti-itd
        # Net Final Balance & Investment
        self.balance_amount = nba-nia
        self.investment_amount = nia
        self.full_clean().save()

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
    user = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='balance_transaction', blank=False
    )
    type_of_transaction = models.CharField(
        max_length=1, choices=TRANSACTION_TYPE, blank=False,
        validators=[validate_balance_type_of_transaction]
    )
    amount = models.DecimalField(
        null=False, blank=False, max_digits=7,
        validators=[validate_amount], decimal_places=2
    )
    verified = models.BinaryField(default=False, editable=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.transaction_user.username + ':' + self.type_of_transaction + ':' + str(self.created)


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
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user + ':' + self.type_of_transaction + ':' + self.pool + ':' + str(self.amount)

    # TODO-NORMAL: Override save method with verified=True to generate & send invoice.


class BillingAddress(models.Model):
    COUNTRY = (
        ('IN', 'India'),
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='address', blank=False)
    name = models.CharField(
        "Full Name", max_length=64, validators=[validate_name],
        help_text="Name of Person for the Address")
    address1 = models.CharField(
        "Address Line 1", max_length=128,
        help_text="Line 1 of the Address")
    address2 = models.CharField(
        "Address Line 2", max_length=128,
        help_text="Line 2 of the Address")
    zip_code = models.CharField(
        "ZIP / Postal code", max_length=12,
        help_text="ZIP / Postal code for the Address")
    city = models.CharField(
        "City", max_length=128,
        help_text="City for the Address")
    state = models.CharField(
        "State", max_length=128,
        help_text="State for the Address")
    country = models.CharField(
        "Country",
        max_length=3,
        choices=COUNTRY)

    def __str__(self):
        return self.name + ', ' + self.address1 + ', ' + self.address2
