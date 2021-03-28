from django.contrib.auth.forms import ValidationError, UsernameField, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account, EmailWhiteList


class EnableTotpForm(forms.ModelForm):

    totp_code = forms.CharField(max_length=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['totp_code'].widget.attrs.update({'autofocus': 'autofocus'})

    class Meta:
        model = Account
        fields = ("totp_code", )


class OurUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(OurUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean(self):
        email = self.cleaned_data.get('email')
        if not EmailWhiteList.objects.filter(email=email).exists():
            raise ValidationError("Email Not Authorized, try another.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account already exists with this email address.")
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Try a different username, that one already exists.")
        return self.cleaned_data


class EditProfileForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    first_name = UsernameField(required=False)
    last_name = UsernameField(required=False)
    twitter_handle = forms.CharField(max_length=64)

    password = forms.CharField(
        label="confirm password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.account = user.account
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data["password"]
        t_handle = self.cleaned_data['twitter_handle']
        if not self.user.check_password(password):
            raise ValidationError("password is incorrect.")
        if email != self.user.email:
            if User.objects.filter(email=email).exists():
                raise ValidationError("An account already exists with this email address.")
        return {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'twitter_handle': t_handle,
        }

    def save(self, commit=True):
        self.user.email = self.cleaned_data['email']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.account.twitter_handle = self.cleaned_data['twitter_handle']
        if commit:
            self.user.save()
            self.account.save()
        return self.user
