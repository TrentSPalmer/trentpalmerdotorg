from django.shortcuts import render, redirect
from .forms import EpisodeForm
from .models import Feed, Episode, rand_slug
from django.utils.text import slugify


def edit_episode(request, pk, title_slug):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    slug = title_slug
    episode = Episode.objects.get(id=pk)
    otitle = episode.title
    if not episode.user == request.user:
        return redirect('audio:home')
    if request.method == "POST":
        form = EpisodeForm(request.POST, request.FILES, instance=episode)
        if form.is_valid():
            nepisode = form.save(commit=False)
            if nepisode.title != otitle:
                nepisode.slug = slugify(rand_slug() + "-" + nepisode.title)
                slug = nepisode.slug
            nepisode.save()
            return redirect('audio:episode', pk=pk, slug=slug)
    else:
        form = EpisodeForm(instance=episode)
    return render(
        request, 'base_form.html',
        {
            'form': form,
            'heading': 'Edit Episode?',
            'title': 'Edit Episode?',
            'submit': 'save',
            'form_data': 'TRUE',
        })


def new_episode(request, feed_pk, feed_title_slug):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    feed = Feed.objects.get(id=feed_pk)
    if not feed.user == request.user:
        return redirect('audio:home')
    if request.method == "POST":
        form = EpisodeForm(request.POST, request.FILES)
        if form.is_valid():
            episode = form.save(commit=False)
            episode.user = request.user
            episode.feed = feed
            episode.save()
            return redirect('audio:feed', pk=feed_pk, slug=feed_title_slug)
    else:
        form = EpisodeForm()
    return render(
        request, 'base_form.html',
        {
            'form': form,
            'heading': 'New Episode?',
            'title': 'New Episode?',
            'submit': 'submit',
            'form_data': 'TRUE',
        })
