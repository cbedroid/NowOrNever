# Generated by Django 3.0.7 on 2020-09-08 09:50

import core.utils.utils_models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("countrycuzzins", "0022_auto_20200908_0539"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                default="nothing",
                null=True,
                storage=core.utils.utils_models.OverwriteStorage(),
                upload_to="images/thumbnails/",
            ),
        ),
    ]
