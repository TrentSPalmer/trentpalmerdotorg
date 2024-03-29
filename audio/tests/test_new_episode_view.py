from django.test import TestCase
from django.contrib.auth.models import User
from audio.tests.test_views import set_up
from audio.models import Episode, Feed
from django.urls import reverse
from datetime import date


class TestNewEpisodeViewTestCase(TestCase):

    def setUp(self):
        set_up()

    def test_new_episode_view_get(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'feed_pk': feed_a.pk, 'feed_title_slug': feed_a.slug}
        response = self.client.get(reverse('audio:new_episode', kwargs=kw_args))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertFalse(Episode.objects.filter(
            title="Mark Twain Taming The Bicycle",
        ).exists())
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/new-episode/{feed_a.pk}/{feed_a.slug}'
        )

    def test_new_episode_view_wrong_user(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        self.client.login(username='user_a', password='password_user_a')
        kw_args = {'feed_pk': feed_a.pk, 'feed_title_slug': feed_a.slug}
        pub_date = str(date.today())
        with (
                open('bicycle.jpg', 'rb') as image_f,
                open('Mark Twain Taming The Bicycle.mp3', 'rb') as mp3_f
        ):
            response = self.client.post(reverse('audio:new_episode', kwargs=kw_args), {
                'title': "Mark Twain Taming The Bicycle",
                'author': "Mark Twain",
                'pub_date': pub_date,
                'episode_number': 3,
                'description': 'learn how to ride a bicycle',
                'mp3': mp3_f,
                'image_title': 'A Penny Farthing',
                'image_attribution': 'Agnieszka Kwiecień',
                'image_attribution_url': 'https://commons.wikimedia.org/wiki/User:Nova',
                'original_image_url': 'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg',
                'image_license': 1,
                'image_license_jurisdiction': 'in the USA',
                'image': image_f,
            }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Episode.objects.filter(
            title="Mark Twain Taming The Bicycle",
        ).exists())
        self.assertEquals(response.request['PATH_INFO'], '/')
        self.assertTemplateUsed(response, 'audio/index.html')

    def test_new_episode_view_no_data(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'feed_pk': feed_a.pk, 'feed_title_slug': feed_a.slug}
        response = self.client.post(reverse('audio:new_episode', kwargs=kw_args))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        qs = Episode.objects.filter(title="Mark Twain Taming The Bicycle")
        self.assertEquals(len(qs), 0)
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/new-episode/{feed_a.pk}/{feed_a.slug}'
        )

    def test_new_episode_view_no_login(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        kw_args = {'feed_pk': feed_a.pk, 'feed_title_slug': feed_a.slug}
        pub_date = str(date.today())
        with (
                open('bicycle.jpg', 'rb') as image_f,
                open('Mark Twain Taming The Bicycle.mp3', 'rb') as mp3_f
        ):
            response = self.client.post(reverse('audio:new_episode', kwargs=kw_args), {
                'title': "Mark Twain Taming The Bicycle",
                'author': "Mark Twain",
                'pub_date': pub_date,
                'episode_number': 3,
                'description': 'learn how to ride a bicycle',
                'mp3': mp3_f,
                'image_title': 'A Penny Farthing',
                'image_attribution': 'Agnieszka Kwiecień',
                'image_attribution_url': 'https://commons.wikimedia.org/wiki/User:Nova',
                'original_image_url': 'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg',
                'image_license': 1,
                'image_license_jurisdiction': 'in the USA',
                'image': image_f,
            }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        qs = Episode.objects.filter(title="Mark Twain Taming The Bicycle")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_new_episode_view(self):
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        user_b = User.objects.get(username='user_b')
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'feed_pk': feed_a.pk, 'feed_title_slug': feed_a.slug}
        pub_date = str(date.today())
        with (
                open('bicycle.jpg', 'rb') as image_f,
                open('Mark Twain Taming The Bicycle.mp3', 'rb') as mp3_f
        ):
            response = self.client.post(reverse('audio:new_episode', kwargs=kw_args), {
                'title': "Mark Twain Taming The Bicycle",
                'author': "Mark Twain",
                'pub_date': pub_date,
                'episode_number': 3,
                'description': 'learn how to ride a bicycle',
                'mp3': mp3_f,
                'image_title': 'A Penny Farthing',
                'image_attribution': 'Agnieszka Kwiecień',
                'image_attribution_url': 'https://commons.wikimedia.org/wiki/User:Nova',
                'original_image_url': 'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg',
                'image_license': 1,
                'image_license_jurisdiction': 'in the USA',
                'image': image_f,
            })
        self.assertEquals(response.status_code, 302)
        episode_a = Episode.objects.get(title="Mark Twain Taming The Bicycle")
        self.assertEquals(episode_a.author, "Mark Twain")
        self.assertEquals(str(episode_a.pub_date), pub_date)
        self.assertEquals(episode_a.episode_number, 3)
        self.assertEquals(episode_a.description, 'learn how to ride a bicycle')
        self.assertEquals(episode_a.image_title, 'A Penny Farthing')
        self.assertEquals(episode_a.image_attribution, 'Agnieszka Kwiecień')
        self.assertEquals(
            episode_a.image_attribution_url, 'https://commons.wikimedia.org/wiki/User:Nova'
        )
        self.assertEquals(
            episode_a.original_image_url,
            'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg'
        )
        self.assertEquals(episode_a.image_license, 1)
        self.assertEquals(episode_a.image_license_jurisdiction, 'in the USA')
        self.assertEquals(episode_a.image_license_name, 'Public Domain')
        self.assertEquals(
            episode_a.image_license_url, 'https://en.wikipedia.org/wiki/Public_domain'
        )
        self.assertEquals(episode_a.user, user_b)
        self.assertEquals(episode_a.feed, feed_a)
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/new-episode/{feed_a.pk}/{feed_a.slug}'
        )
