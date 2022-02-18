# Generated by Django 3.2.10 on 2022-02-18 23:46

import audio.models
from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/trent/trentpalmerdotorg/media/audio/images'), upload_to=audio.models.slugify_file_name)),
                ('image_license', models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0'), (6, 'CC BY 1.0'), (7, 'CC0 1.0'), (8, 'CC BY 4.0')], default=2)),
                ('image_title', models.CharField(default='', max_length=255)),
                ('image_attribution', models.CharField(default='', max_length=255)),
                ('image_attribution_url', models.URLField(blank=True, max_length=255)),
                ('original_image_url', models.URLField(default='', max_length=255)),
                ('image_license_jurisdiction', models.TextField(default='(no jurisdiction specified)')),
                ('author_url', models.URLField(default='', max_length=255)),
                ('ebook_title', models.CharField(default='', max_length=255)),
                ('ebook_url', models.URLField(default='', max_length=255)),
                ('translator', models.CharField(blank=True, max_length=255)),
                ('translator_url', models.URLField(blank=True, max_length=255)),
                ('intro_author', models.CharField(blank=True, max_length=255)),
                ('intro_author_url', models.URLField(blank=True, max_length=255)),
                ('license_jurisdiction', models.TextField(blank=True, default='(no jurisdiction specified)')),
                ('license', models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0'), (6, 'CC BY 1.0'), (7, 'CC0 1.0'), (8, 'CC BY 4.0')], default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/trent/trentpalmerdotorg/media/audio/images'), upload_to=audio.models.slugify_file_name)),
                ('image_license', models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0'), (6, 'CC BY 1.0'), (7, 'CC0 1.0'), (8, 'CC BY 4.0')], default=2)),
                ('image_title', models.CharField(default='', max_length=255)),
                ('image_attribution', models.CharField(default='', max_length=255)),
                ('image_attribution_url', models.URLField(blank=True, max_length=255)),
                ('original_image_url', models.URLField(default='', max_length=255)),
                ('image_license_jurisdiction', models.TextField(default='(no jurisdiction specified)')),
                ('pub_date', models.DateField()),
                ('episode_number', models.IntegerField(null=True)),
                ('mp3', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/trent/trentpalmerdotorg/media/audio/mp3'), upload_to=audio.models.slugify_file_name)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio.feed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
