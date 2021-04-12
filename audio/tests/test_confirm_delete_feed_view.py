from django.test import TestCase
from audio.tests.test_views import set_up
from audio.models import Feed, Episode
from django.urls import reverse


class TestConfirmDeleteFeedViewTestCase(TestCase):

    def setUp(self):
        set_up()

    def test_confirm_delete_feed_view(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'pk': feed_a.pk}
        response = self.client.post(
            reverse('audio:confirm_delete_feed', kwargs=kw_args),
            follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/feeds.html')
        qs = Feed.objects.filter(title="Short Stories Mark Twain")
        self.assertEquals(len(qs), 0)
        qs = Episode.objects.filter(title="Mark Twain On Girls")
        self.assertEquals(len(qs), 0)
        qs = Episode.objects.filter(title="Mark Twain The Bee")
        self.assertEquals(len(qs), 0)

    def test_confirm_delete_feed_view_no_login(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        kw_args = {'pk': feed_a.pk}
        response = self.client.post(
            reverse('audio:confirm_delete_feed', kwargs=kw_args),
            follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        qs = Feed.objects.filter(title="Short Stories Mark Twain")
        self.assertEquals(len(qs), 1)
        qs = Episode.objects.filter(title="Mark Twain On Girls")
        self.assertEquals(len(qs), 1)
        qs = Episode.objects.filter(title="Mark Twain The Bee")
        self.assertEquals(len(qs), 1)
