from django.contrib.auth.forms import ValidationError, UsernameField  # , UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account


class EnableTotpForm(forms.ModelForm):

    totp_code = forms.CharField(max_length=6)

    class Meta:
        model = Account
        fields = ("totp_code", )


class EditProfileForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    first_name = UsernameField(required=False)
    last_name = UsernameField(required=False)

    password = forms.CharField(
        label="confirm password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise ValidationError("password is incorrect.")
        if email != self.user.email:
            if User.objects.filter(email=email).exists():
                raise ValidationError("An account already exists with this email address.")
        return {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }

    def save(self, commit=True):
        self.user.email = self.cleaned_data['email']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        if commit:
            self.user.save()
        return self.user
