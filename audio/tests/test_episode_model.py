from django.test import TestCase
from audio.models import Feed, Episode
from django.contrib.auth.models import User
from uuid import UUID
from datetime import datetime, timedelta


class EpisodeModelTestCase(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        feed_a = Feed.objects.create(user=user_a, title='Civil War')
        p_date = datetime.today() - timedelta(days=8)
        Episode.objects.create(
            title='Chapter I', feed=feed_a, user=user_a,
            pub_date=p_date
        )

    def test_episode(self):
        qs = Episode.objects.all()
        self.assertEquals(len(qs), 1)
        episode_a = Episode.objects.get(title='Chapter I')
        self.assertTrue(isinstance(episode_a.pk, UUID))
        self.assertEquals(str(episode_a), episode_a.title)
