from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account
from django.urls import reverse


class EditProfileViewTestCase(TestCase):

    def setUp(self):
        user_a = User(email='user_a@example.com', username='user_a')
        user_a.set_password('password123456donkey')
        user_a.save()
        Account.objects.create(user=user_a)
        User.objects.create(username='user_c', email='user_c@example.com')

    def test_edit_profile_view_email_already_exists(self):
        self.client.login(username='user_a', password='password123456donkey')
        response = self.client.post(reverse('accounts:edit_profile'), {
            'email': 'user_c@example.com',
            'first_name': 'User_a',
            'last_name': 'Smith',
            'twitter_handle': '@user_a',
            'password': 'password123456donkey',
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        user_a = User.objects.get(username='user_a')
        self.assertEquals(user_a.email, 'user_a@example.com')
        self.assertEquals(user_a.first_name, '')
        self.assertEquals(user_a.account.twitter_handle, '@Twitter')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/edit-profile/')
        msg = "An account already exists with this email address."
        self.assertEquals(response.content.decode('utf-8').count(msg), 1)

    def test_edit_profile_view_no_login(self):
        response = self.client.post(reverse('accounts:edit_profile'), {
            'email': 'user_a@example.com',
            'first_name': 'User_a',
            'last_name': 'Smith',
            'twitter_handle': '@user_a',
            'password': 'password123456donkey',
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        user_a = User.objects.get(username='user_a')
        self.assertEquals(user_a.first_name, '')
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_edit_profile_view_no_data(self):
        self.client.login(username='user_a', password='password123456donkey')
        response = self.client.post(reverse('accounts:edit_profile'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        user_a = User.objects.get(username='user_a')
        self.assertEquals(user_a.first_name, '')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/edit-profile/')
        self.assertEquals(response.content.decode('utf-8').count("This field is required."), 3)

    def test_edit_profile_view_invalid_email(self):
        self.client.login(username='user_a', password='password123456donkey')
        response = self.client.post(reverse('accounts:edit_profile'), {
            'email': 'user_afoobar.com',
            'first_name': 'User_a',
            'last_name': 'Smith',
            'twitter_handle': '@user_a',
            'password': 'password123456donkey',
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        user_a = User.objects.get(username='user_a')
        self.assertEquals(user_a.first_name, '')
        self.assertEquals(user_a.account.twitter_handle, '@Twitter')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/edit-profile/')

    def test_edit_profile_view_invalid_twitter_handle(self):
        self.client.login(username='user_a', password='password123456donkey')
        response = self.client.post(reverse('accounts:edit_profile'), {
            'email': 'user_a@example.com',
            'first_name': 'User_a',
            'last_name': 'Smith',
            'twitter_handle': 'user_a',
            'password': 'password123456donkey',
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        user_a = User.objects.get(username='user_a')
        self.assertEquals(user_a.first_name, '')
        self.assertEquals(user_a.account.twitter_handle, '@Twitter')
        self.assertEquals(response.request['PATH_INFO'], '/accounts/edit-profile/')
        t_warning = "twitter_handle must begin with &quot;@&quot;"
        self.assertTrue(t_warning in response.content.decode('utf-8'))

    def test_edit_profile_view(self):
        self.client.login(username='user_a', password='password123456donkey')
        response = self.client.post(reverse('accounts:edit_profile'), {
            'email': 'user_a@example.com',
            'first_name': 'User_a',
            'last_name': 'Smith',
            'twitter_handle': '@user_a',
            'password': 'password123456donkey',
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        user_a = User.objects.get(username='user_a')
        self.assertEquals(user_a.first_name, 'User_a')
        self.assertEquals(user_a.last_name, 'Smith')
        self.assertEquals(user_a.account.twitter_handle, '@user_a')
        self.assertEquals(response.request['PATH_INFO'], '/')
