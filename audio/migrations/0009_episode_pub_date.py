# Generated by Django 3.1.6 on 2021-02-23 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0008_auto_20210223_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='pub_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]