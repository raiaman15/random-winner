from PIL import Image
from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model

from .models import BalanceTransaction


class ProfileIdentityProofUploadViewForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = get_user_model()
        fields = ('identity_proof', 'x', 'y', 'width', 'height',)

    def save(self):
        user_identity = super(ProfileIdentityProofUploadViewForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(user_identity.identity_proof)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((660, 420), Image.ANTIALIAS)
        resized_image.save(user_identity.identity_proof.path)

        return user_identity


class ProfilePictureViewForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = get_user_model()
        fields = ('picture', 'x', 'y', 'width', 'height')

    def save(self):
        user_profile = super(ProfilePictureViewForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(user_profile.picture)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(user_profile.picture.path)

        return user_profile


class AccountResetPasswordWithOTPViewForm(forms.Form):
    username = forms.CharField()
    captcha = CaptchaField()


class AccountResetPasswordWithOTPConfirmViewForm(forms.Form):
    otp = forms.CharField()


class ManagerProfileApprovePoolmasterViewForm(forms.Form):
    confirm = forms.BooleanField(label='Approve as Master')


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'aadhaar_number', 'pan_number', 'identity_proof',
                  'picture', 'identity_verified', 'contact_verified', 'is_willing_master', 'groups')


class BalanceTransactionAdmin(forms.ModelForm):
    class Meta:
        model = BalanceTransaction
        fields = ('verified',)
