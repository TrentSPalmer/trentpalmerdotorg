# Generated by Django 3.1.6 on 2021-02-22 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0003_auto_20210221_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]