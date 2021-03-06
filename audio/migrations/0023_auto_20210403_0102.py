# Generated by Django 3.1.7 on 2021-04-03 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0022_auto_20210317_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='image_license',
            field=models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0'), (6, 'CC BY 1.0'), (7, 'CC0 1.0')], default=2),
        ),
        migrations.AlterField(
            model_name='feed',
            name='image_license',
            field=models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0'), (6, 'CC BY 1.0'), (7, 'CC0 1.0')], default=2),
        ),
        migrations.AlterField(
            model_name='feed',
            name='license',
            field=models.SmallIntegerField(choices=[(1, 'Public Domain'), (2, 'Unknown'), (3, 'CC BY-SA 2.5'), (4, 'CC BY-SA 3.0'), (5, 'CC BY 3.0'), (6, 'CC BY 1.0'), (7, 'CC0 1.0')], default=1),
        ),
    ]
