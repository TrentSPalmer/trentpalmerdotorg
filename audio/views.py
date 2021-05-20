from django.shortcuts import render, reverse
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from .models import Feed, Episode
from tp.settings import IMAGES_URL, MP3_URL


def home(request):
    episodes = Episode.objects.all().order_by('-pub_date')
    return render(
        request,
        'audio/index.html',
        {
            'episodes': episodes, 'IMAGES_URL': IMAGES_URL,
            'MP3_URL': MP3_URL, 'add_feed_link': True})


def feed(request, pk, slug):
    feed = Feed.objects.get(id=pk)
    episodes = feed.episode_set.all().order_by('-pub_date')
    return render(
        request, 'audio/index.html',
        {
            'episodes': episodes, 'IMAGES_URL': IMAGES_URL, 'view': 'feed',
            'MP3_URL': MP3_URL, 'title': feed.title, 'heading': feed.title,
            'feed_pk': pk, 'feed_slug': slug,
        })


def episode(request, pk, slug):
    episode = Episode.objects.get(id=pk)
    ogurl = reverse('audio:episode', kwargs={'pk': pk, 'slug': slug})
    og_url = f'{get_current_site(request)}{ogurl}'
    return render(
        request, 'audio/index.html',
        {
            'episodes': (episode, ), 'IMAGES_URL': IMAGES_URL, 'is_episode': True,
            'MP3_URL': MP3_URL, 'title': episode.title, 'heading': episode.title,
            'ogtitle': episode.title, 'ogurl': og_url, 'ogmp3': episode.mp3,
            'feed': episode.feed, 'twitter_image': episode.image,
        })


def feeds(request):
    feeds = Feed.objects.all().order_by('-created_on')
    return render(
        request,
        'audio/feeds.html',
        {'feeds': feeds, 'IMAGES_URL': IMAGES_URL})


def feed_list_api(request):
    feeds = Feed.objects.all().order_by('created_on')
    result = []
    for feed in feeds:
        result.append({
            'title': feed.title,
            'read_by': feed.user.username,
            'rss_feed': f'{get_current_site(request)}' + reverse('audio:rss', kwargs={'slug': feed.slug})
        })
    return JsonResponse(result, safe=False)
