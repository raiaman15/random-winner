from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import ContactNumberOTP, BalanceTransaction
from .forms import CustomUserAdminForm

CustomUser = get_user_model()


@admin.register(get_user_model())
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ('first_name', 'last_name', 'email', 'aadhaar_number', 'identity_proof', 'identity_verified',
                    'username', 'contact_verified', 'is_willing_master', 'is_verified_master', 'balance_amount', 'investment_amount')
    list_filter = ('identity_verified', 'contact_verified',
                   'is_willing_master', 'is_verified_master')
    search_fields = ('first_name__startswith', 'last_name__startswith')

    class Meta:
        ordering = ('first_name', 'last_name')


@admin.register(ContactNumberOTP)
class ContactNumberOTPAdmin(admin.ModelAdmin):
    list_display = ('username', 'otp', 'created_at')

    class Meta:
        ordering = ('username')


@admin.register(BalanceTransaction)
class BalanceTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'transaction_amount',
                    'transaction_user', 'created_at')

    class Meta:
        ordering = ()
