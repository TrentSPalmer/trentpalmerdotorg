# Generated by Django 3.1.7 on 2021-02-24 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0009_episode_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='episode_number',
            field=models.IntegerField(null=True),
        ),
    ]