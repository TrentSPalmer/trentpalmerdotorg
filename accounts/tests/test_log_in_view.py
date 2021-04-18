from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestLogInViewTestCase(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        user_a.set_password('password_user_a')
        user_a.save()

    def test_log_in_view_wrong_password(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'user_a',
            'password': 'password_user_b',
        })
        self.assertEquals(response.status_code, 200)
        self.assertFalse("Successfully logged in" in response.content.decode('utf-8'))
        user_a = User.objects.get(username='user_a')
        self.assertFalse(hasattr(user_a, 'account'))
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/login/')
        self.assertEquals(response.content.decode('utf-8').count(
            "Please enter a correct username and password."), 1)

    def test_log_in_view_wrong_user(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'user_b',
            'password': 'password_user_a',
        })
        self.assertEquals(response.status_code, 200)
        self.assertFalse("Successfully logged in" in response.content.decode('utf-8'))
        user_a = User.objects.get(username='user_a')
        self.assertFalse(hasattr(user_a, 'account'))
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/login/')
        self.assertEquals(response.content.decode('utf-8').count(
            "Please enter a correct username and password."), 1)

    def test_log_in_view_no_data(self):
        response = self.client.post(reverse('accounts:login'))
        self.assertEquals(response.status_code, 200)
        self.assertFalse("Successfully logged in" in response.content.decode('utf-8'))
        user_a = User.objects.get(username='user_a')
        self.assertFalse(hasattr(user_a, 'account'))
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/login/')
        self.assertEquals(response.content.decode('utf-8').count("This field is required."), 2)

    def test_log_in_view_already_logged_in(self):
        self.client.login(username='user_a', password='password_user_a')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'user_a',
            'password': 'password_user_a',
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertFalse("Successfully logged in" in response.content.decode('utf-8'))
        user_a = User.objects.get(username='user_a')
        self.assertFalse(hasattr(user_a, 'account'))
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_log_in_view(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'user_a',
            'password': 'password_user_a',
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("Successfully logged in" in response.content.decode('utf-8'))
        user_a = User.objects.get(username='user_a')
        self.assertTrue(hasattr(user_a, 'account'))
        self.assertEquals(user_a.account.twitter_handle, '@Twitter')
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')
