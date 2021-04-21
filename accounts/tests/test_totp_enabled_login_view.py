from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Account
import pyotp
from time import time


class TestTOTPEnabledLogInViewTestCase(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        user_a.set_password('password_user_a')
        user_a.save()
        Account.objects.create(
            user=user_a,
            use_totp=True, totp_key=pyotp.random_base32())

    def test_TOTP_enabled_log_in_view_already_logged_in(self):
        self.client.login(username='user_a', password='password_user_a')
        user_a = User.objects.get(username='user_a')
        totp_code = pyotp.TOTP(user_a.account.totp_key).now()
        response = self.client.post(reverse('accounts:two_factor_input'), {
            'totp_code': totp_code}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_TOTP_enabled_log_in_view_wrong_code_with_retries(self):
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'user_a',
            'password': 'password_user_a',
        }, follow=True)
        self.assertEquals(login_response.status_code, 200)
        self.assertTemplateUsed(login_response, 'accounts/totp_form.html')
        self.assertEquals(login_response.request['PATH_INFO'], '/accounts/two-factor-input/')
        start_a = time()
        response_a = self.client.post(reverse('accounts:two_factor_input'), {
            'totp_code': '666666'}, follow=True)
        self.assertEquals(response_a.status_code, 200)
        self.assertTemplateUsed(response_a, 'accounts/totp_form.html')
        self.assertEquals(response_a.request['PATH_INFO'], '/accounts/two-factor-input/')
        msg = 'Wrong Code, try again?'
        self.assertEquals(response_a.content.decode('utf-8').count(msg), 1)
        start_b = time()
        response_b = self.client.post(reverse('accounts:two_factor_input'), {
            'totp_code': '555555'}, follow=True)
        self.assertEquals(response_b.status_code, 200)
        self.assertTemplateUsed(response_b, 'accounts/totp_form.html')
        self.assertEquals(response_b.request['PATH_INFO'], '/accounts/two-factor-input/')
        msg = 'Wrong Code, try again?'
        self.assertEquals(response_b.content.decode('utf-8').count(msg), 1)
        start_c = time()
        response_c = self.client.post(reverse('accounts:two_factor_input'), {
            'totp_code': '6666'}, follow=True)
        self.assertEquals(response_c.status_code, 200)
        self.assertTemplateUsed(response_c, 'accounts/totp_form.html')
        self.assertEquals(response_c.request['PATH_INFO'], '/accounts/two-factor-input/')
        msg = 'Wrong Code, try again?'
        self.assertEquals(response_c.content.decode('utf-8').count(msg), 1)
        end_c = time()
        self.assertTrue((start_b - start_a) > 1)
        self.assertTrue((start_c - start_b) > 2)
        self.assertTrue((end_c - start_c) > 4)

    def test_TOTP_enabled_log_in_view_no_data_with_retries(self):
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'user_a',
            'password': 'password_user_a',
        }, follow=True)
        self.assertEquals(login_response.status_code, 200)
        self.assertTemplateUsed(login_response, 'accounts/totp_form.html')
        self.assertEquals(login_response.request['PATH_INFO'], '/accounts/two-factor-input/')
        response_a = self.client.post(reverse('accounts:two_factor_input'))
        self.assertEquals(response_a.status_code, 200)
        self.assertTemplateUsed(response_a, 'accounts/totp_form.html')
        self.assertEquals(response_a.request['PATH_INFO'], '/accounts/two-factor-input/')
        msg = 'This field is required.'
        self.assertEquals(response_a.content.decode('utf-8').count(msg), 1)
        response_b = self.client.post(reverse('accounts:two_factor_input'))
        self.assertEquals(response_b.status_code, 200)
        self.assertTemplateUsed(response_b, 'accounts/totp_form.html')
        self.assertEquals(response_b.request['PATH_INFO'], '/accounts/two-factor-input/')
        msg = 'This field is required.'
        self.assertEquals(response_b.content.decode('utf-8').count(msg), 1)
        response_c = self.client.post(reverse('accounts:two_factor_input'))
        self.assertEquals(response_c.status_code, 200)
        self.assertTemplateUsed(response_c, 'accounts/totp_form.html')
        self.assertEquals(response_c.request['PATH_INFO'], '/accounts/two-factor-input/')
        msg = 'This field is required.'
        self.assertEquals(response_c.content.decode('utf-8').count(msg), 1)

    def test_TOTP_enabled_log_in_view_wrong_code(self):
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'user_a',
            'password': 'password_user_a',
        }, follow=True)
        self.assertEquals(login_response.status_code, 200)
        self.assertTemplateUsed(login_response, 'accounts/totp_form.html')
        self.assertEquals(login_response.request['PATH_INFO'], '/accounts/two-factor-input/')
        response = self.client.post(reverse('accounts:two_factor_input'), {
            'totp_code': '666666'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/totp_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/two-factor-input/')
        msg = 'Wrong Code, try again?'
        self.assertEquals(response.content.decode('utf-8').count(msg), 1)

    def test_TOTP_enabled_log_in_view_no_data(self):
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'user_a',
            'password': 'password_user_a',
        }, follow=True)
        self.assertEquals(login_response.status_code, 200)
        self.assertTemplateUsed(login_response, 'accounts/totp_form.html')
        self.assertEquals(login_response.request['PATH_INFO'], '/accounts/two-factor-input/')
        response = self.client.post(reverse('accounts:two_factor_input'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/totp_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/two-factor-input/')
        msg = 'This field is required.'
        self.assertEquals(response.content.decode('utf-8').count(msg), 1)

    def test_TOTP_enabled_log_in_view(self):
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'user_a',
            'password': 'password_user_a',
        }, follow=True)
        self.assertEquals(login_response.status_code, 200)
        self.assertTemplateUsed(login_response, 'accounts/totp_form.html')
        self.assertEquals(login_response.request['PATH_INFO'], '/accounts/two-factor-input/')
        user_a = User.objects.get(username='user_a')
        totp_code = pyotp.TOTP(user_a.account.totp_key).now()
        response = self.client.post(reverse('accounts:two_factor_input'), {
            'totp_code': totp_code}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')
        msg = 'Successfully logged in!'
        self.assertEquals(response.content.decode('utf-8').count(msg), 1)

    def test_two_factor_input_view_not_coming_from_login(self):
        get_response = self.client.get(reverse('accounts:two_factor_input'), follow=True)
        self.assertEquals(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'audio/index.html')
        self.assertEquals(get_response.request['PATH_INFO'], '/')
