# Generated by Django 3.1.7 on 2021-03-16 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0014_auto_20210316_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='image_attribution',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='episode',
            name='image_attribution_url',
            field=models.URLField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='episode',
            name='image_license',
            field=models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0')], default=2),
        ),
        migrations.AddField(
            model_name='episode',
            name='image_license_jurisdiction',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='episode',
            name='image_title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='episode',
            name='original_image_url',
            field=models.URLField(default='', max_length=255),
        ),
    ]
