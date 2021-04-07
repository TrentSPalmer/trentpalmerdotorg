from django.test import TestCase
from uuid import UUID
from accounts.models import EmailWhiteList


class EmailWhiteListModelTest(TestCase):

    def setUp(self):
        email_a = EmailWhiteList(email='user_a@example.com')
        email_a.save()
        EmailWhiteList.objects.create(email='user_b@example.com')

    def test_email(self):
        white_listed_emails = EmailWhiteList.objects.all()

        self.assertTrue(len(white_listed_emails) == 2)

        email_a = white_listed_emails.filter(pk=1)
        self.assertTrue(len(email_a) == 0)

        for i, x in enumerate(white_listed_emails):
            self.assertTrue(isinstance(white_listed_emails[i].pk, UUID))
            self.assertTrue(isinstance(white_listed_emails[i].email, str))
