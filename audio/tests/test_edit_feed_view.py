from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from audio.tests.test_views import set_up
from audio.models import Feed


class TestEditFeedViewTestCase(TestCase):

    def setUp(self):
        set_up()

    def test_edit_feed_view_no_login(self):
        feed_c = Feed.objects.get(title="Short Stories Mark Twain")
        kw_args = {'pk': feed_c.pk, 'title_slug': feed_c.slug}
        with open('bicycle.jpg', 'rb') as image_f:
            response = self.client.post(reverse('audio:edit_feed', kwargs=kw_args), {
                'title': feed_c.title,
                'author': "Mark Twain",
                'ebook_title': "What Is Man? and Other Essays",
                'ebook_url': "https://gutenberg.org/ebooks/70",
                'author_url': "http://gutenberg.org/ebooks/author/53",
                'translator': 'McDevitte, W. A. (William Alexander)',
                'translator_url': 'https://gutenberg.org/ebooks/author/37952',
                'intro_author': 'De Quincey, Thomas',
                'intro_author_url': 'https://gutenberg.org/ebooks/author/797',
                'license': 1,
                'license_jurisdiction': 'in the USA',
                'description': 'Short stories by Mark Twain.',
                'image_title': 'A Penny Farthing',
                'image_attribution': 'Agnieszka Kwiecień',
                'image_attribution_url': 'https://commons.wikimedia.org/wiki/User:Nova',
                'original_image_url': 'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg',
                'image_license': 1,
                'image_license_jurisdiction': 'in the USA',
                'image': image_f,
            })
        self.assertEquals(response.status_code, 302)
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        user_b = User.objects.get(username='user_b')
        self.assertEquals(feed_a.user, user_b)
        self.assertEquals(feed_a.author, "")
        self.assertEquals(feed_a.ebook_title, "")
        self.assertEquals(feed_a.ebook_url, "")
        self.assertEquals(feed_a.author_url, "")
        self.assertEquals(feed_a.translator, "")
        self.assertEquals(feed_a.translator_url, "")
        self.assertEquals(feed_a.intro_author, "")
        self.assertEquals(feed_a.intro_author_url, "")
        self.assertEquals(feed_a.license, 1)
        self.assertEquals(feed_a.license_jurisdiction, "(no jurisdiction specified)")
        self.assertEquals(feed_a.description, "")
        self.assertEquals(feed_a.image_title, "")
        self.assertEquals(feed_a.image_attribution, "")
        self.assertEquals(feed_a.image_attribution_url, "")
        self.assertEquals(feed_a.original_image_url, "")
        self.assertEquals(feed_a.image_license, 2)
        self.assertEquals(feed_a.image_license_jurisdiction, "(no jurisdiction specified)")
        self.assertEquals(feed_a.image_license_url, "https://example.com")
        self.assertEquals(feed_a.image_license_name, 'Unknown')
        self.assertEquals(feed_a.license_url, "https://en.wikipedia.org/wiki/Public_domain")
        self.assertEquals(feed_a.license_name, 'Public Domain')
        self.assertEquals(feed_a.get_itpc_rss, f'itpc://{settings.DOMAIN_NAME}/rss/{feed_a.slug}.xml')
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/edit-feed/{feed_a.pk}/{feed_a.slug}'
        )

    def test_edit_feed_view_no_data(self):
        feed_c = Feed.objects.get(title="Short Stories Mark Twain")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'pk': feed_c.pk, 'title_slug': feed_c.slug}
        response = self.client.post(reverse('audio:edit_feed', kwargs=kw_args))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        user_b = User.objects.get(username='user_b')
        self.assertEquals(feed_a.user, user_b)
        self.assertEquals(feed_a.author, "")
        self.assertEquals(feed_a.ebook_title, "")
        self.assertEquals(feed_a.ebook_url, "")
        self.assertEquals(feed_a.author_url, "")
        self.assertEquals(feed_a.translator, "")
        self.assertEquals(feed_a.translator_url, "")
        self.assertEquals(feed_a.intro_author, "")
        self.assertEquals(feed_a.intro_author_url, "")
        self.assertEquals(feed_a.license, 1)
        self.assertEquals(feed_a.license_jurisdiction, "(no jurisdiction specified)")
        self.assertEquals(feed_a.description, "")
        self.assertEquals(feed_a.image_title, "")
        self.assertEquals(feed_a.image_attribution, "")
        self.assertEquals(feed_a.image_attribution_url, "")
        self.assertEquals(feed_a.original_image_url, "")
        self.assertEquals(feed_a.image_license, 2)
        self.assertEquals(feed_a.image_license_jurisdiction, "(no jurisdiction specified)")
        self.assertEquals(feed_a.image_license_url, "https://example.com")
        self.assertEquals(feed_a.image_license_name, 'Unknown')
        self.assertEquals(feed_a.license_url, "https://en.wikipedia.org/wiki/Public_domain")
        self.assertEquals(feed_a.license_name, 'Public Domain')
        self.assertEquals(feed_a.get_itpc_rss, f'itpc://{settings.DOMAIN_NAME}/rss/{feed_a.slug}.xml')
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/edit-feed/{feed_a.pk}/{feed_a.slug}'
        )

    def test_edit_feed_view(self):
        feed_c = Feed.objects.get(title="Short Stories Mark Twain")
        self.client.login(username='user_b', password='password_user_b')
        kw_args = {'pk': feed_c.pk, 'title_slug': feed_c.slug}
        with open('bicycle.jpg', 'rb') as image_f:
            response = self.client.post(reverse('audio:edit_feed', kwargs=kw_args), {
                'title': feed_c.title,
                'author': "Mark Twain",
                'ebook_title': "What Is Man? and Other Essays",
                'ebook_url': "https://gutenberg.org/ebooks/70",
                'author_url': "http://gutenberg.org/ebooks/author/53",
                'translator': 'McDevitte, W. A. (William Alexander)',
                'translator_url': 'https://gutenberg.org/ebooks/author/37952',
                'intro_author': 'De Quincey, Thomas',
                'intro_author_url': 'https://gutenberg.org/ebooks/author/797',
                'license': 1,
                'license_jurisdiction': 'in the USA',
                'description': 'Short stories by Mark Twain.',
                'image_title': 'A Penny Farthing',
                'image_attribution': 'Agnieszka Kwiecień',
                'image_attribution_url': 'https://commons.wikimedia.org/wiki/User:Nova',
                'original_image_url': 'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg',
                'image_license': 1,
                'image_license_jurisdiction': 'in the USA',
                'image': image_f,
            })
        self.assertEquals(response.status_code, 302)
        feed_a = Feed.objects.get(title="Short Stories Mark Twain")
        user_b = User.objects.get(username='user_b')
        self.assertEquals(feed_a.user, user_b)
        self.assertEquals(feed_a.author, "Mark Twain")
        self.assertEquals(feed_a.ebook_title, "What Is Man? and Other Essays")
        self.assertEquals(feed_a.ebook_url, "https://gutenberg.org/ebooks/70")
        self.assertEquals(feed_a.author_url, "http://gutenberg.org/ebooks/author/53")
        self.assertEquals(feed_a.translator, "McDevitte, W. A. (William Alexander)")
        self.assertEquals(feed_a.translator_url, "https://gutenberg.org/ebooks/author/37952")
        self.assertEquals(feed_a.intro_author, "De Quincey, Thomas")
        self.assertEquals(feed_a.intro_author_url, "https://gutenberg.org/ebooks/author/797")
        self.assertEquals(feed_a.license, 1)
        self.assertEquals(feed_a.license_jurisdiction, "in the USA")
        self.assertEquals(feed_a.description, "Short stories by Mark Twain.")
        self.assertEquals(feed_a.image_title, "A Penny Farthing")
        self.assertEquals(feed_a.image_attribution, "Agnieszka Kwiecień")
        self.assertEquals(feed_a.image_attribution_url, "https://commons.wikimedia.org/wiki/User:Nova")
        self.assertEquals(feed_a.original_image_url, "https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg")
        self.assertEquals(feed_a.image_license, 1)
        self.assertEquals(feed_a.image_license_jurisdiction, "in the USA")
        self.assertEquals(feed_a.image, 'bicycle.jpg')
        self.assertEquals(feed_a.image_license_url, "https://en.wikipedia.org/wiki/Public_domain")
        self.assertEquals(feed_a.image_license_name, 'Public Domain')
        self.assertEquals(feed_a.license_url, "https://en.wikipedia.org/wiki/Public_domain")
        self.assertEquals(feed_a.license_name, 'Public Domain')
        self.assertEquals(feed_a.get_itpc_rss, f'itpc://{settings.DOMAIN_NAME}/rss/{feed_a.slug}.xml')
        self.assertEquals(
            response.request['PATH_INFO'],
            f'/edit-feed/{feed_a.pk}/{feed_a.slug}'
        )
