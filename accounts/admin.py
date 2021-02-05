from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import ContactNumberOTP, BalanceTransaction, BillingAddress
from .forms import CustomUserAdminForm

CustomUser = get_user_model()


@admin.register(get_user_model())
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ('username', 'first_name', 'last_name', 'email', 'aadhaar_number', 'identity_proof',
                    'identity_verified', 'contact_verified', 'is_willing_master')
    list_filter = ('identity_verified',
                   'contact_verified', 'is_willing_master')
    search_fields = ('username__startswith', 'first_name__startswith',
                     'last_name__startswith')

    class Meta:
        ordering = ('first_name', 'last_name')


@admin.register(ContactNumberOTP)
class ContactNumberOTPAdmin(admin.ModelAdmin):
    list_display = ('username', 'created')
    search_fields = ('username__startswith',)

    class Meta:
        ordering = ('username',)


@admin.register(BalanceTransaction)
class BalanceTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type_of_transaction',
                    'amount', 'created', 'verified')
    list_filter = ('verified', 'type_of_transaction')
    search_fields = ('user__startswith',)

    class Meta:
        ordering = ('created')


@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address1', 'address2',
                    'zip_code', 'city', 'state', 'country')

    class Meta:
        ordering = ('country', 'state', 'city', 'zipcode')
