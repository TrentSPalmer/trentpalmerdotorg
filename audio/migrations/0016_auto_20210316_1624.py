# Generated by Django 3.1.7 on 2021-03-16 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0015_auto_20210316_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='image_license',
            field=models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0'), (6, 'CC BY 1.0')], default=2),
        ),
        migrations.AlterField(
            model_name='feed',
            name='image_license',
            field=models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0'), (6, 'CC BY 1.0')], default=2),
        ),
    ]
