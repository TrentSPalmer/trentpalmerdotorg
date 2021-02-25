from django.db import models
from tp.models import UUIDAsIDModel
from django.contrib.auth.models import User


class Account(UUIDAsIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    totp_key = models.CharField(max_length=16, null=True)
    use_totp = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
