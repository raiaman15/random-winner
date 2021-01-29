import pyotp
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from config.validators import validate_aadhaar_number


class CustomUser(AbstractUser):
    USER_TYPE = (
        ('MM', 'Manager'),
        ('MA', 'Master'),
        ('ME', 'Member')
    )
    user_type = models.CharField(
        max_length=2, choices=USER_TYPE, default='ME', blank=True
    )
    picture = models.ImageField(
        upload_to='picture/', blank=True,
        help_text='Your recent picture (must match with picture in photo ID below) in .png or .jpg format.'
    )
    aadhaar_number = models.CharField(
        max_length=12, validators=[validate_aadhaar_number], blank=True,
        help_text='Your 12 digit Aadhaar Number (as written on your aadhaar card).'
    )
    identity_proof = models.ImageField(
        upload_to='identity/', blank=True,
        help_text='Your photo ID proof (preferably Aadhaar Card) in .png or .jpg format.'
    )
    identity_verified = models.BooleanField(default=False)
    contact_number = models.CharField(
        max_length=17, blank=True, help_text='Your valid mobile number for OTP verification.'
    )
    contact_secret = models.CharField(max_length=16, blank=True)
    contact_verified = models.BooleanField(default=False)
    is_willing_master = models.BooleanField(default=False)
    is_verified_master = models.BooleanField(default=False)
    balance_amount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2)
    investment_amount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2)

    def generate_otp(self):
        self.contact_secret = pyotp.random_base32()
        totp = pyotp.TOTP(self.contact_secret, interval=60)
        PhoneNumberOTP(contact_number=self.contact_number, otp=totp).save()

    def apply_for_master(self):
        if self.identity_verified and self.contact_verified:
            self.is_willing_master = True

    def apply_for_withdrawal(self, amount):
        if self.identity_verified and self.contact_verified:
            pass
            # TODO-NORMAL: Raise request for admin.

    def __str__(self):
        return self.email


class PhoneNumberOTP(models.Model):
    contact_number = models.CharField(
        max_length=17, blank=False, unique=True, editable=False
    )
    otp = models.CharField(
        max_length=6, blank=False, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)


class BalanceTransaction(models.Model):
    TRANSACTION_TYPE = (
        ('D', 'Deposit'),
        ('W', 'Withdraw')
    )
    transaction_type = models.CharField(
        max_length=1, choices=TRANSACTION_TYPE, blank=False
    )
    transaction_amount = models.DecimalField(
        null=False, blank=False, max_digits=7, decimal_places=2
    )
    transaction_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='balance_transactions', blank=False
    )

    def __str__(self):
        return self.transaction_by.email + ':' + self.transaction_type + ':' + self.transaction_amount
