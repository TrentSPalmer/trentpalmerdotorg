from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account
from uuid import UUID


class UserModelTestCase(TestCase):

    def setUp(self):
        user_a = User(email='user_a@example.com', username='user_a')
        user_a.set_password('password123456')
        user_a.save()
        user_b = User(email='user_b@example.com', username='user_b')
        user_b.set_password('123456password')
        user_b.save()
        Account.objects.create(user=user_a, twitter_handle='@user_a')
        Account.objects.create(user=user_b)

    def test_user(self):
        test_users = User.objects.all()
        for i, x in enumerate(test_users):
            self.assertTrue(isinstance(test_users[i].email, str))
            self.assertTrue(isinstance(test_users[i].username, str))

        user_a = User.objects.get(username='user_a')
        account_a = Account.objects.get(user=user_a)
        self.assertTrue(user_a.check_password('password123456'))
        self.assertTrue(account_a.user.check_password('password123456'))
        self.assertFalse(user_a.check_password('foo'))
        self.assertFalse(account_a.user.check_password('foo'))
        self.assertEqual(user_a.pk, 1)
        self.assertEqual(account_a.twitter_handle, '@user_a')
        self.assertTrue(account_a.totp_key is None)
        self.assertFalse(account_a.use_totp)
        self.assertTrue(isinstance(account_a.pk, UUID))

        user_b = User.objects.get(username='user_b')
        account_b = Account.objects.get(user=user_b)
        self.assertTrue(user_b.check_password('123456password'))
        self.assertTrue(account_b.user.check_password('123456password'))
        self.assertFalse(user_b.check_password('bar'))
        self.assertFalse(account_b.user.check_password('bar'))
        self.assertEqual(user_b.pk, 2)
        self.assertEqual(account_b.twitter_handle, '@Twitter')
        self.assertTrue(user_b.account.totp_key is None)
        self.assertFalse(user_b.account.use_totp)
        self.assertTrue(isinstance(user_b.account.pk, UUID))
