from .models import Feed, Episode
from django import forms


class FeedForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = [
            'title', 'author', 'description', 'image'
        ]


class EpisodeForm(forms.ModelForm):

    pub_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Episode
        fields = [
            'title', 'author', 'pub_date', 'episode_number', 'description', 'image', 'mp3'
        ]
