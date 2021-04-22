from django.test import TestCase
from django.urls import reverse
from audio.tests.test_views import set_up
from audio.models import Episode


class TestEditEpisodeViewTestCase(TestCase):

    def setUp(self):
        set_up()

    def test_edit_episode_view_wrong_user(self):
        episode_a = Episode.objects.get(title="Mark Twain The Bee")
        self.client.login(username='user_a', password='password_user_a')
        kw_args = {'pk': episode_a.pk, 'title_slug': episode_a.slug}
        response = self.client.post(reverse('audio:edit_episode', kwargs=kw_args), {
            'title': episode_a.title,
            'author': "Mark Twain",
            'pub_date': episode_a.pub_date,
            'episode_number': 2,
            'description': "An essay about the human quality of bees.",
            'image_title': "Stenotritus pubescens",
            'image_attribution': "USGS Bee Inventory and Monitoring Lab",
            'original_image_url': "https://www.flickr.com/photos/usgsbiml/14589580124/",
            'image_license': 1,
            'image_license_jurisdiction': "in the United States",
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        episode_ab = Episode.objects.get(title="Mark Twain The Bee")
        self.assertEquals(episode_ab.author, "")
        self.assertIsNone(episode_ab.episode_number)
        self.assertEquals(episode_ab.description, "")
        self.assertEquals(episode_ab.image_attribution, "")
        self.assertEquals(episode_ab.original_image_url, "")
        self.assertEquals(episode_ab.image_license, 2)
        self.assertEquals(episode_ab.image_license_jurisdiction, "(no jurisdiction specified)")
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_edit_episode_view(self):
        episode_a = Episode.objects.get(title="Mark Twain The Bee")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'pk': episode_a.pk, 'title_slug': episode_a.slug}
        response = self.client.post(reverse('audio:edit_episode', kwargs=kw_args), {
            'title': episode_a.title,
            'author': "Mark Twain",
            'pub_date': episode_a.pub_date,
            'episode_number': 2,
            'description': "An essay about the human quality of bees.",
            'image_title': "Stenotritus pubescens",
            'image_attribution': "USGS Bee Inventory and Monitoring Lab",
            'original_image_url': "https://www.flickr.com/photos/usgsbiml/14589580124/",
            'image_license': 1,
            'image_license_jurisdiction': "in the United States",
        })
        self.assertEquals(response.status_code, 302)
        episode_ab = Episode.objects.get(title="Mark Twain The Bee")
        self.assertEquals(episode_ab.author, "Mark Twain")
        self.assertEquals(episode_ab.episode_number, 2)
        self.assertEquals(episode_ab.description, "An essay about the human quality of bees.")
        self.assertEquals(episode_ab.image_attribution, "USGS Bee Inventory and Monitoring Lab")
        self.assertEquals(
            episode_ab.original_image_url,
            "https://www.flickr.com/photos/usgsbiml/14589580124/"
        )
        self.assertEquals(episode_ab.image_license, 1)
        self.assertEquals(episode_ab.image_license_jurisdiction, "in the United States")
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/edit-episode/{episode_ab.pk}/{episode_ab.slug}'
        )

    def test_edit_episode_view_no_data(self):
        episode_a = Episode.objects.get(title="Mark Twain The Bee")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'pk': episode_a.pk, 'title_slug': episode_a.slug}
        response = self.client.post(reverse('audio:edit_episode', kwargs=kw_args))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        episode_ab = Episode.objects.get(title="Mark Twain The Bee")
        self.assertEquals(episode_ab.author, '')
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/edit-episode/{episode_ab.pk}/{episode_ab.slug}'
        )

    def test_edit_episode_view_no_login(self):
        episode_a = Episode.objects.get(title="Mark Twain The Bee")
        kw_args = {'pk': episode_a.pk, 'title_slug': episode_a.slug}
        response = self.client.post(reverse('audio:edit_episode', kwargs=kw_args), {
            'title': episode_a.title,
            'author': "Twain Mark",
            'pub_date': episode_a.pub_date,
            'episode_number': 2,
            'description': "An essay about the human quality of bees.",
            'image_title': "Stenotritus pubescens",
            'image_attribution': "USGS Bee Inventory and Monitoring Lab",
            'original_image_url': "https://www.flickr.com/photos/usgsbiml/14589580124/",
            'image_license': 1,
            'image_license_jurisdiction': "in the United States",
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        episode_ab = Episode.objects.get(title="Mark Twain The Bee")
        self.assertEquals(episode_ab.author, "")
        self.assertEquals(response.request['PATH_INFO'], '/')
