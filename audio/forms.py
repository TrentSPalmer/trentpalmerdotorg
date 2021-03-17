from .models import Feed, Episode
from django import forms


class FeedForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = [
            'title', 'author', 'ebook_title', 'ebook_url',
            'author_url', 'translator', 'translator_url',
            'intro_author', 'intro_author_url', 'license', 'license_jurisdiction',
            'description', 'image_title', 'image_attribution',
            'image_attribution_url', 'original_image_url', 'image_license',
            'image_license_jurisdiction', 'image'
        ]


class EpisodeForm(forms.ModelForm):

    pub_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Episode
        fields = [
            'title', 'author', 'pub_date', 'episode_number',
            'description', 'mp3',
            'image_title', 'image_attribution', 'image_attribution_url',
            'original_image_url', 'image_license',
            'image_license_jurisdiction', 'image'
        ]
