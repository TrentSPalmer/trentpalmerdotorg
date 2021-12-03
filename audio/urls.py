from django.urls import path
from . import views
from .episode_views import new_episode, edit_episode, confirm_delete_episode
from .feed_views import new_feed, edit_feed, confirm_delete_feed
from .audiorssfeed import AudioRssFeed

app_name = "audio"

urlpatterns = [
    path('', views.home, name='home'),
    path('new-feed/', new_feed, name='new_feed'),
    path('feeds/', views.feeds, name='feeds'),
    path('edit-feed/<str:pk>/<str:title_slug>', edit_feed, name='edit_feed'),
    path(
        'confirm-delete-feed/<str:pk>', confirm_delete_feed,
        name='confirm_delete_feed'
    ),
    path(
        'confirm-delete-episode/<str:pk>', confirm_delete_episode,
        name='confirm_delete_episode'
    ),
    path(
        'new-episode/<str:feed_pk>/<str:feed_title_slug>', new_episode,
        name='new_episode'
    ),
    path(
        'edit-episode/<str:pk>/<str:title_slug>', edit_episode,
        name='edit_episode'
    ),
    path('rss/<str:slug>.xml', AudioRssFeed(), name='rss'),
    path('feed/<str:pk>/<str:slug>', views.feed, name='feed'),
    path('episode/<str:pk>/<str:slug>', views.episode, name='episode'),
    path('feed-list-api/', views.feed_list_api, name='feed_list_api')
]
