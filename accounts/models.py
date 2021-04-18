from django.db import models
from tp.models import UUIDAsIDModel
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def twitter_handle_validator(x):
    if x[0] != '@':
        raise ValidationError('twitter_handle must begin with "@"')


class EmailWhiteList(UUIDAsIDModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Account(UUIDAsIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    totp_key = models.CharField(max_length=16, null=True)
    use_totp = models.BooleanField(default=False)
    twitter_handle = models.CharField(max_length=64, default='@Twitter')

    def __str__(self):
        return str(self.user)
