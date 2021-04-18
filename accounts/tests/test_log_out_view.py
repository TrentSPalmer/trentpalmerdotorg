from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestLogOutViewTestCase(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        user_a.set_password('password_user_a')
        user_a.save()

    def test_log_out_view(self):
        self.client.login(username='user_a', password='password_user_a')
        response = self.client.post(reverse('accounts:logout'), follow=True)
        self.assertTrue("Successfully Logged Out" in response.content.decode('utf-8'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_log_out_view_no_login(self):
        response = self.client.post(reverse('accounts:logout'), follow=True)
        self.assertFalse("Successfully Logged Out" in response.content.decode('utf-8'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')
