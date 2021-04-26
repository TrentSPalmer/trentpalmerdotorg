from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from audio.models import Feed, Episode
from datetime import date, timedelta
from audio.rss_utils import get_rss_item_desc
from bs4 import BeautifulSoup
from tp.settings import IMAGES_URL


class TestGetRssItemDescTestCase(TestCase):

    def test_get_rss_item_desc(self):
        episode_a = Episode.objects.get(title="Caesar-Pompey Civil War Book I")
        desc = get_rss_item_desc(episode_a)
        soup = BeautifulSoup(desc, features="lxml")
        body = soup.find('body')
        bc = body.findChildren(recursive=False)
        self.assertEquals(len(bc), 6)
        self.assertEquals(str(bc[0]), f'<h1>{episode_a.title}</h1>')
        self.assertEquals(str(bc[1]), f'<img src="{IMAGES_URL}{episode_a.image.name}"/>')
        self.assertEquals(str(bc[2]), f'<p>{episode_a.description}</p>')
        bc3a = f'<p>Photo <a href="{episode_a.feed.original_image_url}">'
        bc3b = f'{episode_a.feed.image_title}</a> by {episode_a.feed.image_attribution}'
        bc3c = f' is licensed <a href="{episode_a.feed.image_license_url}">'
        bc3d = f'{episode_a.feed.image_license_name}</a> {episode_a.feed.image_license_jurisdiction}.</p>'
        self.assertEquals(str(bc[3]), f'{bc3a}{bc3b}{bc3c}{bc3d}')
        bc4a = f'<p>Photo <a href="{episode_a.original_image_url}">'
        bc4b = f'{episode_a.image_title}</a> by {episode_a.image_attribution}'
        bc4c = f' is licensed <a href="{episode_a.image_license_url}">'
        bc4d = f'{episode_a.image_license_name}</a> {episode_a.image_license_jurisdiction}.</p>'
        self.assertEquals(str(bc[4]), f'{bc4a}{bc4b}{bc4c}{bc4d}')
        bc5a = f'<p><a href="{episode_a.feed.ebook_url}">{episode_a.feed.ebook_title}</a>'.replace('&', '&amp;')
        bc5b = f' by <a href="{episode_a.feed.author_url}">{episode_a.feed.author}</a>'
        bc5c = f' is licensed <a href="{episode_a.feed.license_url}">'
        bc5d = f'{episode_a.feed.license_name}</a> {episode_a.feed.license_jurisdiction}.</p>'
        self.assertEquals(str(bc[5]), f'{bc5a}{bc5b}{bc5c}{bc5d}')

    def setUp(self):
        user_a = User.objects.create(username='user_a')
        user_a.set_password('password_user_a')
        user_a.save()
        self.client.login(username='user_a', password='password_user_a')
        with open('bicycle.jpg', 'rb') as image_f:
            self.client.post(reverse('audio:new_feed'), {
                'title': "Caesar-Pompey Civil War",
                'author': "Gaius Julius Caesar",
                'ebook_title': "Caesar's De Bello Gallico & Other Commentaries",
                'ebook_url': "https://gutenberg.org/ebooks/10657",
                'author_url': "https://gutenberg.org/ebooks/author/3621",
                'license': 1,
                'license_jurisdiction': 'in the USA',
                'description': "Civil War between Pompey and Caesar.",
                'image_title': 'A Penny Farthing',
                'image_attribution': 'Agnieszka Kwiecień',
                'original_image_url': 'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg',
                'image_license': 1,
                'image_license_jurisdiction': 'in the USA',
                'image': image_f,
            })
        feed_a = Feed.objects.get(title='Caesar-Pompey Civil War')
        kw_args = {'feed_pk': feed_a.pk, 'feed_title_slug': feed_a.slug}
        with (
                open('bicycle.jpg', 'rb') as image_f,
                open('Mark Twain Taming The Bicycle.mp3', 'rb') as mp3_f
        ):
            self.client.post(reverse('audio:new_episode', kwargs=kw_args), {
                'title': "Caesar-Pompey Civil War Book I",
                'author': "Gaius Julius Caesar",
                'pub_date': str(date.today() - timedelta(days=8)),
                'episode_number': 1,
                'description': 'Caesar confronts Afranius and Petreius',
                'mp3': mp3_f,
                'image_title': 'A Penny Farthing',
                'image_attribution': 'Agnieszka Kwiecień',
                'original_image_url': 'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg',
                'image_license': 1,
                'image_license_jurisdiction': 'in the USA',
                'image': image_f,
            })
        with (
                open('bicycle.jpg', 'rb') as image_f,
                open('Mark Twain Taming The Bicycle.mp3', 'rb') as mp3_f
        ):
            self.client.post(reverse('audio:new_episode', kwargs=kw_args), {
                'title': "Caesar-Pompey Civil War Book II",
                'author': "Gaius Julius Caesar",
                'pub_date': str(date.today() - timedelta(days=7)),
                'episode_number': 2,
                'description': 'Trebonius confronts Domitius',
                'mp3': mp3_f,
                'image_title': 'A Penny Farthing',
                'image_attribution': 'Agnieszka Kwiecień',
                'image_attribution_url': 'https://commons.wikimedia.org/wiki/User:Nova',
                'original_image_url': 'https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg',
                'image_license': 1,
                'image_license_jurisdiction': 'in the USA',
                'image': image_f,
            })
