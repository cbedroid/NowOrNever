# Generated by Django 3.0.7 on 2020-07-23 12:21

import countrycuzzins.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0071_auto_20200723_0819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='le',
        ),
        migrations.AddField(
            model_name='song',
            name='file',
            field=models.FileField(default='1', upload_to=countrycuzzins.models.toNameSpace, verbose_name='song file'),
        ),
    ]
