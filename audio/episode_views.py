from django.shortcuts import render, redirect
from .forms import EpisodeForm
from .models import Feed, Episode


def edit_episode(request, pk, title_slug):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    episode = Episode.objects.get(id=pk)
    if not episode.user == request.user:
        return redirect('audio:home')
    if request.method == "POST":
        form = EpisodeForm(request.POST, request.FILES, instance=episode)
        if form.is_valid():
            form.save()
            return redirect('audio:home')
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
            return redirect('audio:new_feed')
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
