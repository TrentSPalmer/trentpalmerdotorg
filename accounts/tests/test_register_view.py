from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account, EmailWhiteList
from django.urls import reverse


class RegisterViewTestCase(TestCase):

    def setUp(self):
        user_b = User(email='user_b@example.com', username='user_b')
        user_b.set_password('123456password')
        user_b.save()
        user_c = User(username='user_c')
        user_c.set_password('123456password')
        user_c.save()
        Account.objects.create(user=user_b, twitter_handle='@user_b')
        Account.objects.create(user=user_c)
        EmailWhiteList.objects.create(email='user_a@example.com')
        EmailWhiteList.objects.create(email='user_b@example.com')
        EmailWhiteList.objects.create(email='user_c@example.com')

    def test_register_user_already_exists(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'user_c',
            'email': 'user_c@example.com',
            'password1': 'password123456donkey',
            'password2': 'password123456donkey'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        qs = User.objects.filter(username="user_a")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/accounts/register/')
        msg = "Try a different username, that one already exists."
        self.assertEquals(response.content.decode('utf-8').count(msg), 1)

    def test_register_email_already_exists(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'user_a',
            'email': 'user_b@example.com',
            'password1': 'password123456donkey',
            'password2': 'password123456donkey'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        qs = User.objects.filter(username="user_a")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/accounts/register/')
        msg = "An account already exists with this email address."
        self.assertEquals(response.content.decode('utf-8').count(msg), 1)

    def test_register_already_logged_in(self):
        self.client.login(username='user_b', password='123456password')
        response = self.client.post(reverse('accounts:register'), {
            'username': 'user_a',
            'email': 'user_a@example.com',
            'password1': 'password123456donkey',
            'password2': 'password123456donkey'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        qs = User.objects.filter(username="user_a")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_register_email_no_data(self):
        response = self.client.post(reverse('accounts:register'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        qs = User.objects.filter(username="user_a")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/accounts/register/')
        self.assertTrue("Email Not Authorized, try another." in response.content.decode('utf-8'))
        self.assertEquals(response.content.decode('utf-8').count("This field is required."), 4)

    def test_register_email_not_authorized(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'user_a',
            'email': 'user_a@foobar.com',
            'password1': 'password123456donkey',
            'password2': 'password123456donkey'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        qs = User.objects.filter(username="user_a")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/accounts/register/')
        self.assertTrue("Email Not Authorized, try another." in response.content.decode('utf-8'))

    def test_register_passwords_dont_match(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'user_a',
            'email': 'user_a@example.com',
            'password1': 'password123456donkey',
            'password2': 'password123donkey456'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        qs = User.objects.filter(username="user_a")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/accounts/register/')
        self.assertTrue("The two password fields didn’t match." in response.content.decode('utf-8'))

    def test_register_password_too_common(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'user_a',
            'email': 'user_a@example.com',
            'password1': 'password123456',
            'password2': 'password123456'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        qs = User.objects.filter(username="user_a")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/accounts/register/')
        self.assertTrue("This password is too common." in response.content.decode('utf-8'))

    def test_register(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'user_a',
            'email': 'user_a@example.com',
            'password1': 'password123456donkey',
            'password2': 'password123456donkey'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        user_a = User.objects.get(username="user_a")
        self.assertEquals(user_a.email, 'user_a@example.com')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/login/')
        self.assertTrue(user_a.check_password('password123456donkey'))
