from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from audio.models import Feed, Episode
from datetime import datetime, timedelta


def set_up():
    user_a = User.objects.create(username='user_a')
    user_a.set_password('password_user_a')
    user_a.save()
    user_b = User.objects.create(username='user_b')
    user_b.set_password('password_user_b')
    user_b.save()
    feed_a = Feed.objects.create(user=user_a, title='Caesar-Pompey Civil War')
    feed_b = Feed.objects.create(
        user=user_a, title="Caesar's De Bello Gallico & Other Commentaries"
    )
    feed_c = Feed.objects.create(user=user_b, title="Short Stories Mark Twain")
    Episode.objects.create(
        user=user_a, feed=feed_a, title="Caesar-Pompey Civil War Book I",
        pub_date=datetime.today() - timedelta(days=8)
    )
    Episode.objects.create(
        user=user_a, feed=feed_a, title="Caesar-Pompey Civil War Book II",
        pub_date=datetime.today() - timedelta(days=7)
    )
    Episode.objects.create(
        user=user_a, feed=feed_b,
        title="De Bello Gallico & Other Commentaries Book I",
        pub_date=datetime.today() - timedelta(days=6)
    )
    Episode.objects.create(
        user=user_a, feed=feed_b, title="De Bello Gallico & Other Commentaries Book II",
        pub_date=datetime.today() - timedelta(days=5)
    )
    Episode.objects.create(
        user=user_b, feed=feed_c, title="Mark Twain On Girls",
        pub_date=datetime.today() - timedelta(days=4)
    )
    Episode.objects.create(
        user=user_b, feed=feed_c, title="Mark Twain The Bee",
        pub_date=datetime.today() - timedelta(days=3)
    )


class TestViewsTestCase(TestCase):

    def setUp(self):
        set_up()

    def test_home_view(self):
        response = self.client.get(reverse('audio:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')

    def test_feed_view(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        kw_args = {'pk': feed_a.pk, 'slug': feed_a.slug}
        response = self.client.get(reverse('audio:feed', kwargs=kw_args))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')

    def test_episode_view(self):
        episode_a = Episode.objects.get(title='Mark Twain The Bee')
        kw_args = {'pk': episode_a.pk, 'slug': episode_a.slug}
        response = self.client.get(reverse('audio:episode', kwargs=kw_args))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')

    def test_feeds_view(self):
        response = self.client.get(reverse('audio:feeds'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/feeds.html')
