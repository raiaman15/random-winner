import pyotp
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, DecimalValidator
from config.validators import validate_aadhaar_number, validate_pan_number, validate_conatct_number, validate_amount, validate_otp, validate_balance_transaction_type
from config.utils import send_otp


class CustomUser(AbstractUser):
    picture = models.ImageField(
        upload_to='picture/', blank=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        help_text='Your recent picture (must match with picture in photo ID below) in .png or .jpg format. (Max 2 MB)'
    )
    aadhaar_number = models.CharField(
        max_length=12, validators=[validate_aadhaar_number], blank=True,
        help_text='Your 12 digit Aadhaar Number (as written on your aadhaar card).'
    )
    pan_number = models.CharField(
        max_length=10, validators=[validate_pan_number], blank=True,
        help_text='Your 10 digit PAN Number (as written on your PAN card).'
    )
    identity_proof = models.ImageField(
        upload_to='identity/', blank=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        help_text='Your photo ID proof (preferably Aadhaar Card) in .png or .jpg format. (Max 2 MB)'
    )
    identity_verified = models.BooleanField(default=False)
    identity_reject_reason = models.CharField(
        max_length=250, blank=True,
        help_text='Your 10 digit PAN Number (as written on your PAN card).'
    )
    contact_number = models.CharField(
        max_length=12, blank=True,
        validators=[validate_conatct_number],
        help_text='Your valid mobile number for OTP verification.'
    )
    contact_secret = models.CharField(max_length=16, blank=True)
    contact_verified = models.BooleanField(default=False)
    is_willing_master = models.BooleanField(default=False)
    is_verified_master = models.BooleanField(default=False)
    balance_amount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2,
        validators=[DecimalValidator, validate_amount]
    )
    investment_amount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2,
        validators=[DecimalValidator, validate_amount]
    )

    def generate_otp(self):
        self.contact_secret = pyotp.random_base32()
        totp = pyotp.TOTP(self.contact_secret, interval=125).now()
        send_otp(self.contact_number, totp)
        ContactNumberOTP(contact_number=self.contact_number, otp=totp).save()
        return True

    def apply_for_master(self):
        if self.identity_verified and self.contact_verified:
            self.is_willing_master = True

    def apply_for_withdrawal(self, amount):
        if self.identity_verified and self.contact_verified:
            pass
            # TODO-NORMAL: Raise request for admin.

    def __str__(self):
        return self.contact_number


class ContactNumberOTP(models.Model):
    contact_number = models.CharField(
        max_length=17, blank=False, unique=True,
        validators=[validate_conatct_number], editable=False
    )
    otp = models.CharField(
        max_length=6, blank=False,
        validators=[validate_otp], editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class BalanceTransaction(models.Model):
    TRANSACTION_TYPE = (
        ('D', 'Debit'),
        ('C', 'Credit')
    )
    transaction_type = models.CharField(
        max_length=1, choices=TRANSACTION_TYPE, blank=False,
        validators=[validate_balance_transaction_type]
    )
    transaction_amount = models.DecimalField(
        null=False, blank=False, max_digits=7,
        validators=[validate_amount], decimal_places=2
    )
    transaction_user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='balance_transactions', blank=False
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.transaction_user.contact_number + ':' + self.transaction_type + ':' + str(self.transaction_amount)
