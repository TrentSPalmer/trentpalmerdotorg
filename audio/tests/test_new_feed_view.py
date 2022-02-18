from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from audio.models import Feed, Episode
from datetime import datetime, timedelta
from django.urls import reverse


class TestNewFeedViewTestCase(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        user_a.set_password('password_user_a')
        user_a.save()
        user_b = User.objects.create(username='user_b')
        user_b.set_password('password_user_b')
        user_b.save()
        feed_a = Feed.objects.create(user=user_a, title='Caesar-Pompey Civil War')
        Episode.objects.create(
            user=user_a, feed=feed_a, title="Caesar-Pompey Civil War Book I",
            pub_date=datetime.today() - timedelta(days=8)
        )
        Episode.objects.create(
            user=user_a, feed=feed_a, title="Caesar-Pompey Civil War Book II",
            pub_date=datetime.today() - timedelta(days=7)
        )

    def test_new_feed_view_get(self):
        self.client.login(username='user_b', password='password_user_b')
        response = self.client.get(reverse('audio:new_feed'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        self.assertEquals(response.request['PATH_INFO'], '/new-feed/')

    def test_new_feed_view_no_data(self):
        self.client.login(username='user_b', password='password_user_b')
        response = self.client.post(reverse('audio:new_feed'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_form.html')
        qs = Feed.objects.filter(title="Short Stories Mark Twain")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/new-feed/')

    def test_new_feed_view_no_login(self):
        with open('bicycle.jpg', 'rb') as image_f:
            response = self.client.post(reverse('audio:new_feed'), {
                'title': "Short Stories Mark Twain",
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
            }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio/index.html')
        qs = Feed.objects.filter(title="Short Stories Mark Twain")
        self.assertEquals(len(qs), 0)
        self.assertEquals(response.request['PATH_INFO'], '/')

    def test_new_feed_view(self):
        self.client.login(username='user_b', password='password_user_b')
        with open('bicycle.jpg', 'rb') as image_f:
            response = self.client.post(reverse('audio:new_feed'), {
                'title': "Short Stories Mark Twain",
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
        self.assertEquals(feed_a.image_license_url, "https://en.wikipedia.org/wiki/Public_domain")
        self.assertEquals(feed_a.image_license_name, 'Public Domain')
        self.assertEquals(feed_a.license_url, "https://en.wikipedia.org/wiki/Public_domain")
        self.assertEquals(feed_a.license_name, 'Public Domain')
        self.assertEquals(feed_a.get_itpc_rss, f'itpc://{settings.DOMAIN_NAME}/rss/{feed_a.slug}.xml')
        self.assertEquals(response.request['PATH_INFO'], '/new-feed/')
