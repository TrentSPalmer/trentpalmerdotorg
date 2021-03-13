from django.shortcuts import render, redirect
from .forms import FeedForm
from .models import Feed, rand_slug
from django.contrib import messages
from django.utils.text import slugify


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


def confirm_delete_feed(request, pk):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    feed = Feed.objects.get(id=pk)
    if not feed.user == request.user:
        return redirect('audio:home')
    if request.method == 'POST':
        feed.delete()
        messages.success(request, f'Feed {feed.title} deleted!', extra_tags='mb-0')
        return redirect('audio:feeds')
    return render(request, 'audio/delete_feed_confirmation.html', {
        'title': 'Delete Feed?',
        'heading': 'Delete Feed?',
        'feed': feed})


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
            'edit_feed': True,
            'feed_pk': pk,
        })
