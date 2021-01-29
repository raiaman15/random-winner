from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserAdminForm

CustomUser = get_user_model()


@admin.register(get_user_model())
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ('email', 'username', 'date_joined', 'kyc_verified', 'phone_verified',
                    'is_willing_master', 'is_verified_master', 'balance_amount', 'investment_amount')
    list_filter = ('kyc_verified', 'phone_verified',
                   'is_willing_master', 'is_verified_master')
    search_fields = ('first_name__startswith', 'last_name__startswith')

    class Meta:
        ordering = ('first_name', 'last_name')
