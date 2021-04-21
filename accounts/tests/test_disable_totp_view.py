from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account
from django.urls import reverse
import pyotp


class TestDisableTOTPViewTestCase(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        user_a.set_password('password_user_a')
        user_a.save()
        Account.objects.create(user=user_a)
        user_b = User.objects.create(username='user_b')
        user_b.set_password('password_user_b')
        user_b.save()
        Account.objects.create(
            user=user_b,
            use_totp=True, totp_key=pyotp.random_base32())

    def test_disable_totp_view_get(self):
        self.client.login(username='user_b', password='password_user_b')
        response = self.client.get(reverse('accounts:disable_totp'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirmation.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/disable-totp/')

    def test_disable_totp_view_no_login(self):
        response = self.client.post(reverse('accounts:disable_totp'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_disable_totp_view_not_enabled(self):
        self.client.login(username='user_a', password='password_user_a')
        response = self.client.post(reverse('accounts:disable_totp'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_disable_totp_view(self):
        self.client.login(username='user_b', password='password_user_b')
        response = self.client.post(reverse('accounts:disable_totp'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/edit-profile/')
        user_b = User.objects.get(username='user_b')
        self.assertFalse(user_b.account.use_totp)
        self.assertIsNone(user_b.account.totp_key)
        msg = "Thanks for disabling 2fa!"
        self.assertEquals(response.content.decode('utf-8').count(msg), 1)
