# Generated by Django 3.0.7 on 2020-07-23 10:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0064_auto_20200723_0634'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='image',
            field=models.ForeignKey(default='2020-07-23 10:36:08.374781+00:00', on_delete=django.db.models.deletion.DO_NOTHING, related_name='album_image', to='countrycuzzins.Image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='album',
            name='slug',
            field=models.SlugField(default='Album_url', help_text='<p style="color:red; font-weight:700;"> DO NOT ADD DASHES</p>', max_length=80, unique=True, validators=[django.core.validators.MinLengthValidator(4)], verbose_name='album url'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='album',
            name='songs',
            field=models.ManyToManyField(help_text='<p style="color:#000; font-weight:700;"> Select ALL songs that will be on album</p>', to='countrycuzzins.Song', verbose_name='list of songs'),
        ),
    ]
