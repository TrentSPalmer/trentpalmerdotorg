from django.test import TestCase
from django.contrib.auth.models import User


class UserModelTest(TestCase):

    def setUp(self):
        user_a = User(email='user_a@example.com', username='user_a')
        user_a.set_password('password123456')
        user_a.save()
        user_b = User(email='user_b@example.com', username='user_b')
        user_b.set_password('123456password')
        user_b.save()

    def test_user(self):
        test_users = User.objects.all()
        for i, x in enumerate(test_users):
            self.assertTrue(isinstance(test_users[i].email, str))
            self.assertTrue(isinstance(test_users[i].username, str))

        user_a = User.objects.get(username='user_a')
        self.assertTrue(user_a.check_password('password123456'))
        self.assertFalse(user_a.check_password('foo'))
        self.assertEqual(user_a.pk, 1)

        user_b = User.objects.get(username='user_b')
        self.assertTrue(user_b.check_password('123456password'))
        self.assertFalse(user_b.check_password('bar'))
        self.assertEqual(user_b.pk, 2)
