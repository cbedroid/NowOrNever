# Generated by Django 3.0.7 on 2020-07-23 12:32

import countrycuzzins.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0082_remove_song_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='file',
            field=models.FileField(default='hello', upload_to=countrycuzzins.models.toNameSpace, verbose_name='song file'),
            preserve_default=False,
        ),
    ]