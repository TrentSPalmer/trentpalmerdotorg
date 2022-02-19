from django.test import TestCase
from django.contrib.auth.models import User
from audio.models import Feed, Episode
from accounts.models import Account
from datetime import date, timedelta
from dateutil import parser
from django.urls import reverse
import xml.etree.ElementTree as ET
from tp.settings import IMAGES_URL, MP3_URL
from .string_test_string import get_ep_description


class TestRssTestCase(TestCase):
    def test_rss(self):
        feed_a = Feed.objects.get(title="Caesar-Pompey Civil War")
        kw_args = {"slug": feed_a.slug}
        response = self.client.get(reverse("audio:rss", kwargs=kw_args))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.templates), 0)
        self.assertEquals(response.request["PATH_INFO"], f"/rss/{feed_a.slug}.xml")
        rss = ET.fromstring(response.content)
        self.assertEquals(rss.attrib["version"], "2.0")
        rss_children = [t.tag for t in rss.findall("*")]
        self.assertEquals(rss_children, ["channel"])
        channel = rss.find("channel")
        channel_children = [t.tag for t in channel.findall("*")]
        self.assertEquals(
            channel_children,
            [
                "title",
                "link",
                "description",
                "{http://www.w3.org/2005/Atom}link",
                "language",
                "lastBuildDate",
                "image",
                "item",
                "item",
            ],
        )
        channel_title = channel.find("title")
        self.assertEquals(channel_title.text, "Caesar-Pompey Civil War")
        cdt = channel.find("description").text
        self.assertEquals(cdt, "Civil War between Pompey and Caesar.")
        channel_link = channel.find("link")
        self.assertEquals(
            channel_link.text[-75:],
            reverse("audio:feed", kwargs={"pk": feed_a.pk, "slug": feed_a.slug}),
        )
        cdlang = channel.find("language").text
        self.assertEquals(cdlang, "en-us")
        latest_post = str(date.today() - timedelta(days=7))
        cdlbd = parser.parse(channel.find("lastBuildDate").text)
        cdlbd_string = cdlbd.strftime("%Y-%m-%d")
        self.assertEquals(latest_post, cdlbd_string)
        f_image = channel.find("image")
        f_image_children = [t.tag for t in f_image.findall("*")]
        self.assertEquals(f_image_children, ["url", "title", "link", "description"])
        f_image_url = f_image.find("url").text
        self.assertEquals(f_image_url, f"{IMAGES_URL}{feed_a.image}")
        f_image_title = f_image.find("title").text
        self.assertEquals(f_image_title, feed_a.title)
        f_image_link = f_image.find("link").text
        self.assertEquals(f_image_link, f"testserver/feed/{feed_a.pk}/{feed_a.slug}")
        f_image_description = f_image.find("description").text
        self.assertEquals(
            f_image_description,
            '<p>Photo <a href="https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg">A Penny Farthing</a> by <a href="https://commons.wikimedia.org/wiki/User:Nova">Agnieszka Kwiecień</a> is licensed <a href="https://en.wikipedia.org/wiki/Public_domain">Public Domain</a> in the USA.</p>',
        )
        episodes = [t for t in channel.findall("item")]
        for i, ep in enumerate(episodes):
            ep_children = [t.tag for t in ep.findall("*")]
            self.assertEquals(
                ep_children,
                [
                    "title",
                    "link",
                    "description",
                    "pubDate",
                    "guid",
                    "enclosure",
                    "image",
                ],
            )
            episode = Episode.objects.get(feed=feed_a, episode_number=i + 1)
            ep_title = ep.find("title").text
            self.assertEquals(ep_title, f"{episode.episode_number}: {episode.title}")
            ep_link = ep.find("link").text
            self.assertEquals(
                ep_link, f"http://testserver/episode/{episode.pk}/{episode.slug}"
            )
            ep_desc = ep.find("description").text
            self.assertEquals(ep_desc, get_ep_description(feed_a, episode))
            ep_pub_date = parser.parse(ep.find("pubDate").text).strftime("%Y-%m-%d")
            self.assertEquals(ep_pub_date, str(episode.pub_date))
            ep_guid = ep.find("guid").text
            self.assertEquals(
                ep_guid, f"http://testserver/episode/{episode.pk}/{episode.slug}"
            )
            ep_enclosure = ep.find("enclosure")
            self.assertEquals(list(ep_enclosure.keys()), ["length", "type", "url"])
            self.assertEquals(ep_enclosure.attrib["length"], str(episode.mp3.size))
            self.assertEquals(ep_enclosure.attrib["type"], "audio/mpeg")
            self.assertEquals(ep_enclosure.attrib["url"], f"{MP3_URL}{episode.mp3}")
            ep_image = ep.find("image")
            epim_children = [t.tag for t in ep_image.findall("*")]
            self.assertEquals(epim_children, ["url", "title", "link", "description"])
            epim_url = ep_image.find("url").text
            self.assertEquals(epim_url, f"{IMAGES_URL}{episode.image.name}")
            epim_title = ep_image.find("title").text
            self.assertEquals(epim_title, episode.title)
            epim_link = ep_image.find("link").text
            self.assertEquals(
                epim_link, f"testserver/episode/{episode.pk}/{episode.slug}"
            )
            epim_desc = ep_image.find("description").text
            self.assertEquals(epim_desc, f"Image for: {episode.title}")

    def setUp(self):
        user_a = User.objects.create(username="user_a")
        user_a.set_password("password_user_a")
        user_a.save()
        Account.objects.create(user=user_a)
        self.client.login(username="user_a", password="password_user_a")
        with open("bicycle.jpg", "rb") as image_f:
            self.client.post(
                reverse("audio:new_feed"),
                {
                    "title": "Caesar-Pompey Civil War",
                    "author": "Gaius Julius Caesar",
                    "ebook_title": "Caesar's De Bello Gallico & Other Commentaries",
                    "ebook_url": "https://gutenberg.org/ebooks/10657",
                    "author_url": "https://gutenberg.org/ebooks/author/3621",
                    "translator": "McDevitte, W. A. (William Alexander)",
                    "translator_url": "https://gutenberg.org/ebooks/author/37952",
                    "intro_author": "De Quincey, Thomas",
                    "intro_author_url": "https://gutenberg.org/ebooks/author/797",
                    "license": 1,
                    "license_jurisdiction": "in the USA",
                    "description": "Civil War between Pompey and Caesar.",
                    "image_title": "A Penny Farthing",
                    "image_attribution": "Agnieszka Kwiecień",
                    "image_attribution_url": "https://commons.wikimedia.org/wiki/User:Nova",
                    "original_image_url": "https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg",
                    "image_license": 1,
                    "image_license_jurisdiction": "in the USA",
                    "image": image_f,
                },
            )
        feed_a = Feed.objects.get(title="Caesar-Pompey Civil War")
        kw_args = {"feed_pk": feed_a.pk, "feed_title_slug": feed_a.slug}
        with (open("bicycle.jpg", "rb") as image_f, open("Mark Twain Taming The Bicycle.mp3", "rb") as mp3_f):
            self.client.post(
                reverse("audio:new_episode", kwargs=kw_args),
                {
                    "title": "Caesar-Pompey Civil War Book I",
                    "author": "Gaius Julius Caesar",
                    "pub_date": str(date.today() - timedelta(days=8)),
                    "episode_number": 1,
                    "description": "Caesar confronts Afranius and Petreius",
                    "mp3": mp3_f,
                    "image_title": "A Penny Farthing",
                    "image_attribution": "Agnieszka Kwiecień",
                    "image_attribution_url": "https://commons.wikimedia.org/wiki/User:Nova",
                    "original_image_url": "https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg",
                    "image_license": 1,
                    "image_license_jurisdiction": "in the USA",
                    "image": image_f,
                },
            )
        with (
            open("bicycle.jpg", "rb") as image_f,
            open("Mark Twain Taming The Bicycle.mp3", "rb") as mp3_f,
        ):
            self.client.post(
                reverse("audio:new_episode", kwargs=kw_args),
                {
                    "title": "Caesar-Pompey Civil War Book II",
                    "author": "Gaius Julius Caesar",
                    "pub_date": str(date.today() - timedelta(days=7)),
                    "episode_number": 2,
                    "description": "Trebonius confronts Domitius",
                    "mp3": mp3_f,
                    "image_title": "A Penny Farthing",
                    "image_attribution": "Agnieszka Kwiecień",
                    "image_attribution_url": "https://commons.wikimedia.org/wiki/User:Nova",
                    "original_image_url": "https://commons.wikimedia.org/wiki/File:Ordinary_bicycle01.jpg",
                    "image_license": 1,
                    "image_license_jurisdiction": "in the USA",
                    "image": image_f,
                },
            )
