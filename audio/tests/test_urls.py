from django.test import SimpleTestCase
from django.urls import reverse, resolve
from audio.urls import urlpatterns
from audio.views import home, feed, episode, feeds
from audio.feed_views import new_feed, confirm_delete_feed, edit_feed
from audio.episode_views import edit_episode, confirm_delete_episode, new_episode


class TestRssUrls(SimpleTestCase):

    def test_audiorssfeed_url_is_resolved(self):
        url = reverse('audio:rss', kwargs={'slug': 'some-test-string'})
        self.assertEquals(resolve(url).url_name, 'rss')


class TestEpisodeViewsUrls(SimpleTestCase):

    def test_edit_episode_url_is_resolved(self):
        url = reverse('audio:edit_episode', kwargs={
            'pk': 'some_test_string', 'title_slug': 'some-test-string'})
        self.assertEquals(resolve(url).func, edit_episode)

    def test_confirm_delete_episode_url_is_resolved(self):
        url = reverse('audio:confirm_delete_episode', kwargs={
            'pk': 'some_test_string'})
        self.assertEquals(resolve(url).func, confirm_delete_episode)

    def test_new_episode_url_is_resolved(self):
        url = reverse('audio:new_episode', kwargs={
            'feed_pk': 'some_test_string', 'feed_title_slug': 'some-test-string'})
        self.assertEquals(resolve(url).func, new_episode)


class TestFeedViewsUrls(SimpleTestCase):

    def test_new_feed_url_is_resolved(self):
        url = reverse('audio:new_feed')
        self.assertEquals(resolve(url).func, new_feed)

    def test_confirm_delete_feed_url_is_resolved(self):
        url = reverse('audio:confirm_delete_feed', kwargs={
            'pk': 'some_test_string'})
        self.assertEquals(resolve(url).func, confirm_delete_feed)

    def test_edit_feed_url_is_resolved(self):
        url = reverse('audio:edit_feed', kwargs={
            'pk': 'some_test_string', 'title_slug': 'some-test-string'})
        self.assertEquals(resolve(url).func, edit_feed)


class TestNumUrls(SimpleTestCase):

    def test_num_urls(self):
        self.assertEquals(len(urlpatterns), 12)


class TestViewsUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('audio:home')
        self.assertEquals(resolve(url).func, home)

    def test_feed_url_is_resolved(self):
        url = reverse('audio:feed', kwargs={
            'pk': 'some_test_string', 'slug': 'some-test-string'})
        self.assertEquals(resolve(url).func, feed)

    def test_episode(self):
        url = reverse('audio:episode', kwargs={
            'pk': 'some_test_string', 'slug': 'some-test-string'})
        self.assertEquals(resolve(url).func, episode)

    def test_feeds_url_is_resolved(self):
        url = reverse('audio:feeds')
        self.assertEquals(resolve(url).func, feeds)
