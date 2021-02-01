from PIL import Image
from django import forms
from django.core.files import File
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'picture', 'identity_proof',
                  'contact_number', 'identity_verified', 'contact_verified')


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('identity_verified', 'is_verified_master',)


class CustomUserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'picture')


class UserProfileForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'picture',
                  'x', 'y', 'width', 'height', )

    def save(self):
        user_profile = super(UserProfileForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(user_profile.picture)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(user_profile.picture.path)

        return user_profile
