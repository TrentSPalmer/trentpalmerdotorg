from django.contrib.syndication.views import Feed as RSSFeed
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from tp.settings import IMAGES_URL, MP3_URL
from .models import Feed
from datetime import datetime


class AudioRssFeedGenerator(Rss201rev2Feed):
    content_type = 'application/xml; charset=utf-8'

    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        handler.startElement("image", {})
        handler.addQuickElement("url", self.feed['image_url'])
        handler.addQuickElement("title", self.feed['image_title'])
        handler.addQuickElement("link", self.feed['image_link'])
        handler.addQuickElement("description", self.feed['image_desc'])
        handler.endElement("image")

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.startElement("image", {})
        handler.addQuickElement("url", item['image_url'])
        handler.addQuickElement("title", item['image_title'])
        handler.addQuickElement("link", item['image_link'])
        handler.addQuickElement("description", item['image_desc'])
        handler.endElement("image")


class AudioRssFeed(RSSFeed):

    feed_type = AudioRssFeedGenerator

    def get_object(self, request, slug):
        obj = Feed.objects.get(slug=slug)
        obj.request = request
        return obj

    def items(self, obj):
        xr = [x for x in obj.episode_set.order_by('pub_date')]
        for x in xr:
            x.request = obj.request
        return xr

    def item_enclosure_url(self, item):
        return f'{MP3_URL}{item.mp3}'

    def item_enclosure_length(self, item):
        return item.image.size

    def item_enclosure_mime_type(self, item):
        return "audio/mpeg"

    def item_pubdate(self, item):
        '''
        Need to return datetime.datetime object,
        but item.pub_date is an datetime.date object
        '''
        return datetime.fromisoformat(item.pub_date.isoformat())

    def link(self, obj):
        return reverse('audio:feed', kwargs={'pk': obj.pk, 'slug': obj.slug})

    def title(self, obj):
        return obj.title

    def description(self, obj):
        return obj.description

    def item_link(self, item):
        return reverse('audio:episode', kwargs={'pk': item.pk, 'slug': item.slug})

    def item_title(self, item):
        return f'{item.episode_number}: {item.title}'

    def item_extra_kwargs(self, item):
        x = {}
        x['image_url'] = f'{IMAGES_URL}{item.image.name}'
        x['image_title'] = item.title
        x['image_link'] = f'{get_current_site(item.request)}{self.item_link(item)}'
        x['image_desc'] = f'Image for: {item.title}'
        return x

    def feed_extra_kwargs(self, obj):
        x = {}
        x['image_url'] = f'{IMAGES_URL}{obj.image.name}'
        x['image_title'] = obj.title
        x['image_link'] = f'{get_current_site(obj.request)}{self.link(obj)}'
        x['image_desc'] = f'Image for: {obj.title}'
        return x
