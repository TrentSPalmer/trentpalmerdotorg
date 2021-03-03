from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from .forms import FeedForm
from django.utils.text import slugify
from .models import Feed, Episode, rand_slug
from tp.settings import IMAGES_URL, MP3_URL


def home(request):
    episodes = Episode.objects.all().order_by('-pub_date')
    return render(
        request,
        'audio/index.html',
        {'episodes': episodes, 'IMAGES_URL': IMAGES_URL, 'MP3_URL': MP3_URL})


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
            'ogtitle': episode.title, 'ogurl': og_url, 'ogmp3': episode.mp3, 'feed': episode.feed
        })


def feeds(request):
    feeds = Feed.objects.all().order_by('-created_on')
    return render(
        request,
        'audio/feeds.html',
        {'feeds': feeds, 'IMAGES_URL': IMAGES_URL})


def new_feed(request):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    if request.method == "POST":
        form = FeedForm(request.POST, request.FILES)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = request.user
            feed.save()
            return redirect('audio:home')
    else:
        form = FeedForm()
    return render(request, 'base_form.html', {'form': form})


def edit_feed(request, pk, title_slug):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    slug = title_slug
    feed = Feed.objects.get(id=pk)
    otitle = feed.title
    if not feed.user == request.user:
        return redirect('audio:home')
    if request.method == "POST":
        form = FeedForm(request.POST, request.FILES, instance=feed)
        if form.is_valid():
            nfeed = form.save(commit=False)
            if nfeed.title != otitle:
                nfeed.slug = slugify(rand_slug() + "-" + nfeed.title)
                slug = nfeed.slug
            nfeed.save()
            return redirect('audio:feed', pk=pk, slug=slug)
    else:
        form = FeedForm(instance=feed)
    return render(
        request, 'base_form.html',
        {
            'form': form,
            'heading': 'Edit Feed?',
            'title': 'Edit Feed?',
            'submit': 'save',
            'form_data': 'TRUE',
        })
