from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


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
    kyc = models.ImageField(
        upload_to='kyc/', blank=True,
        help_text='Your photo ID (preferably Aadhaar Card) in .png or .jpg format.'
    )
    kyc_verified = models.BooleanField(default=False)
    phone = models.CharField(
        max_length=17, blank=True, help_text='Your valid mobile number for OTP verification.'
    )
    phone_verified = models.BooleanField(default=False)
    is_willing_master = models.BooleanField(default=False)
    is_verified_master = models.BooleanField(default=False)
    balance_amount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2)
    investment_amount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2)

    def apply_for_master(self):
        if self.kyc_verified and self.phone_verified:
            self.is_willing_master = True

    def apply_for_withdrawal(self, amount):
        if self.kyc_verified and self.phone_verified:
            pass
            # TODO-NORMAL: Raise request for admin.

    def __str__(self):
        return self.email


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
