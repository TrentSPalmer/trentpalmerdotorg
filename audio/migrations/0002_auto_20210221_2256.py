# Generated by Django 3.1.6 on 2021-02-22 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='author',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='feed',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
