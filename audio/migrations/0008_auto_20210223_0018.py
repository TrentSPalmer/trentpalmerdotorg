# Generated by Django 3.1.6 on 2021-02-23 08:18

import audio.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tp.storage_backends
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('audio', '0007_auto_20210222_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=tp.storage_backends.PublicImageStorage(), upload_to=audio.models.slugify_file_name),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, storage=tp.storage_backends.PublicImageStorage(), upload_to=audio.models.slugify_file_name)),
                ('mp3', models.FileField(blank=True, null=True, storage=tp.storage_backends.PublicMP3Storage(), upload_to=audio.models.slugify_file_name)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio.feed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]