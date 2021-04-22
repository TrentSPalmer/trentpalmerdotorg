from django.test import TestCase
from audio.tests.test_views import set_up
from audio.models import Feed, Episode
from django.urls import reverse


class TestConfirmDeleteFeedViewTestCase(TestCase):

    def setUp(self):
        set_up()

    def test_confirm_delete_feed_view_incorrect_user(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        self.client.login(username='user_a', password='password_user_a')
        kw_args = {'pk': feed_a.pk}
        response = self.client.post(
            reverse('audio:confirm_delete_feed', kwargs=kw_args),
            follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        self.assertEquals(response.request['PATH_INFO'], '/')
        qs = Feed.objects.filter(title="Short Stories Mark Twain")
        self.assertEquals(len(qs), 1)

    def test_confirm_delete_feed_view_get(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'pk': feed_a.pk}
        response = self.client.get(reverse(
            'audio:confirm_delete_feed', kwargs=kw_args))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/delete_feed_confirmation.html')
        qs = Feed.objects.filter(title="Short Stories Mark Twain")
        self.assertEquals(len(qs), 1)
        qs = Episode.objects.filter(title="Mark Twain On Girls")
        self.assertEquals(len(qs), 1)
        qs = Episode.objects.filter(title="Mark Twain The Bee")
        self.assertEquals(len(qs), 1)
        self.assertEquals(response.request['PATH_INFO'], f'/confirm-delete-feed/{feed_a.pk}')

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
        self.assertEquals(response.request['PATH_INFO'], '/feeds/')

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
        self.assertEquals(response.request['PATH_INFO'], '/')
