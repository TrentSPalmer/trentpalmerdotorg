from django.test import TestCase
from audio.models import Feed
from django.contrib.auth.models import User
from uuid import UUID


class FeedModelTestCase(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        Feed.objects.create(user=user_a, title='Civil War')

    def test_feed(self):
        qs = Feed.objects.all()
        self.assertEquals(len(qs), 1)
        feed_a = Feed.objects.get(title='Civil War')
        self.assertTrue(isinstance(feed_a.pk, UUID))
        self.assertEquals(str(feed_a), feed_a.title)
