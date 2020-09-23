# Generated by Django 3.0.7 on 2020-09-08 08:50

import core.utils.utils_models
import countrycuzzins.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("countrycuzzins", "0019_video_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                default="nothing",
                storage=core.utils.utils_models.OverwriteStorage(),
                upload_to=countrycuzzins.models.toNameSpace,
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="thumbnail_choice",
            field=models.IntegerField(
                choices=[(1, 0), (2, 1), (3, 2), (4, 3)],
                default=1,
                verbose_name="choose a thumbnail",
            ),
        ),
    ]
