from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import log_out, password_change, register, edit_profile
from accounts.login import log_in, two_factor_input
from accounts.enable_totp import enable_totp, disable_totp


class TestViewsUrls(SimpleTestCase):

    def test_password_change_url_is_resolved(self):
        url = reverse('accounts:password_change')
        self.assertEquals(resolve(url).func, password_change)

    def test_register_url_is_resolved(self):
        url = reverse('accounts:register')
        self.assertEquals(resolve(url).func, register)

    def test_logout_url_is_resolved(self):
        url = reverse('accounts:logout')
        self.assertEquals(resolve(url).func, log_out)

    def test_edit_profile_url_is_resolved(self):
        url = reverse('accounts:edit_profile')
        self.assertEquals(resolve(url).func, edit_profile)


class TestLoginViewsUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('accounts:login')
        self.assertEquals(resolve(url).func, log_in)

    def test_2fa_url_is_resolved(self):
        url = reverse('accounts:two_factor_input')
        self.assertEquals(resolve(url).func, two_factor_input)


class TestEnableTotpUrls(SimpleTestCase):

    def test_enable_totp_url_is_resolved(self):
        url = reverse('accounts:enable_totp')
        self.assertEquals(resolve(url).func, enable_totp)

    def test_disable_totp_url_is_resolved(self):
        url = reverse('accounts:disable_totp')
        self.assertEquals(resolve(url).func, disable_totp)
