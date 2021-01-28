from django.contrib import admin
from .models import Pool
# from .forms import CustomUserCreationForm, CustomUserChangeForm


class PoolAdmin(admin.ModelAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = Pool
    list_display = ['name', 'master', ]


admin.site.register(Pool, PoolAdmin)
