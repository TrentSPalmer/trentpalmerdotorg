from django.urls import path
from . import views
from .episode_views import new_episode, edit_episode
from .audiorssfeed import AudioRssFeed

app_name = "audio"

urlpatterns = [
    path('', views.home, name='home'),
    path('new-feed/', views.new_feed, name='new_feed'),
    path('feeds/', views.feeds, name='feeds'),
    path('edit-feed/<str:pk>/<str:title_slug>', views.edit_feed, name='edit_feed'),
    path('new-episode/<str:feed_pk>/<str:feed_title_slug>', new_episode, name='new_episode'),
    path('edit-episode/<str:pk>/<str:title_slug>', edit_episode, name='edit_episode'),
    path('rss/<str:slug>.xml', AudioRssFeed(), name='rss'),
    path('feed/<str:pk>/<str:slug>', views.feed, name='feed'),
    path('episode/<str:pk>/<str:slug>', views.episode, name='episode'),
]
