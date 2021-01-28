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
        upload_to='picture/', blank=True
    )
    kyc_document = models.ImageField(
        upload_to='kyc_documents/', blank=True
    )
    is_verified = models.BooleanField(default=False)
    is_willing_master = models.BooleanField(default=False)
    is_verified_master = models.BooleanField(default=False)
    balance_cash = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2)
    balance_investment = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2)

    def apply_for_master(self):
        if self.is_verified and self.kyc_document:
            self.is_willing_master = True

    def apply_for_withdrawal(self, amount):
        if self.is_verified and self.kyc_document:
            pass


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
