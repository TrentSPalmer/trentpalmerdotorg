from django.test import TestCase
from django.urls import reverse
from audio.tests.test_views import set_up
from audio.models import Episode


class TestConfirmDeleteEpisodeViewTestCase(TestCase):

    def setUp(self):
        set_up()

    def test_confirm_delete_episode_view_wrong_user(self):
        episode_a = Episode.objects.get(title="Mark Twain The Bee")
        self.client.login(username='user_a', password='password_user_a')
        kw_args = {'pk': episode_a.pk}
        response = self.client.post(
            reverse('audio:confirm_delete_episode', kwargs=kw_args),
            follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        qs = Episode.objects.filter(title="Mark Twain The Bee")
        self.assertEquals(len(qs), 1)
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_confirm_delete_episode_view_get(self):
        episode_a = Episode.objects.get(title="Mark Twain The Bee")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'pk': episode_a.pk}
        response = self.client.get(
            reverse('audio:confirm_delete_episode', kwargs=kw_args),
            follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/delete_episode_confirmation.html')
        qs = Episode.objects.filter(title="Mark Twain The Bee")
        self.assertEquals(len(qs), 1)
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/confirm-delete-episode/{episode_a.pk}'
        )

    def test_confirm_delete_episode_view(self):
        episode_a = Episode.objects.get(title="Mark Twain The Bee")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'pk': episode_a.pk}
        response = self.client.post(
            reverse('audio:confirm_delete_episode', kwargs=kw_args),
            follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        qs = Episode.objects.filter(title="Mark Twain The Bee")
        self.assertEquals(len(qs), 0)
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/feed/{episode_a.feed.pk}/{episode_a.feed.slug}'
        )

    def test_confirm_delete_episode_view_no_login(self):
        episode_a = Episode.objects.get(title="Mark Twain The Bee")
        kw_args = {'pk': episode_a.pk}
        response = self.client.post(
            reverse('audio:confirm_delete_episode', kwargs=kw_args),
            follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        qs = Episode.objects.filter(title="Mark Twain The Bee")
        self.assertEquals(len(qs), 1)
        self.assertEquals(response.request['PATH_INFO'], '/')
