from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account
from django.urls import reverse


class PasswordChangeViewTestCase(TestCase):

    def setUp(self):
        user_a = User(email='user_a@example.com', username='user_a')
        user_a.set_password('password123456')
        user_a.save()
        Account.objects.create(user=user_a, twitter_handle='@user_a')

    def test_password_change_view_no_login(self):
        response = self.client.post(reverse('accounts:password_change'), {
            'old_password': 'password123456',
            'new_password1': '123456password',
            'new_password2': '123456password'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        user_a = User.objects.get(username='user_a')
        self.assertTrue(user_a.check_password('password123456'))
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_password_change_view_mismatched_passwords(self):
        self.client.login(username='user_a', password='password123456')
        response = self.client.post(reverse('accounts:password_change'), {
            'old_password': 'password123456',
            'new_password1': '123456password',
            'new_password2': '12346password'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        user_a = User.objects.get(username='user_a')
        self.assertTrue(user_a.check_password('password123456'))
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/password-change/')

    def test_password_change_view_bad_password(self):
        self.client.login(username='user_a', password='password123456')
        response = self.client.post(reverse('accounts:password_change'), {
            'old_password': 'password12345',
            'new_password1': '123456password',
            'new_password2': '123456password'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        user_a = User.objects.get(username='user_a')
        self.assertTrue(user_a.check_password('password123456'))
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/password-change/')

    def test_password_change_view(self):
        self.client.login(username='user_a', password='password123456')
        response = self.client.post(reverse('accounts:password_change'), {
            'old_password': 'password123456',
            'new_password1': '123456password',
            'new_password2': '123456password'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        user_a = User.objects.get(username='user_a')
        self.assertTrue(user_a.check_password('123456password'))
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/edit-profile/')
