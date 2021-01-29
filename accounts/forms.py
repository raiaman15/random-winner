from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'picture', 'kyc',
                  'phone', 'kyc_verified', 'phone_verified')


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('kyc_verified', 'is_verified_master',)


class CustomUserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'picture')
