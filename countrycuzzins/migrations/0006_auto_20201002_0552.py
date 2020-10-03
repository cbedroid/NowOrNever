# Generated by Django 3.0.7 on 2020-10-02 09:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0005_video_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(help_text='<span id="myslughelp"></span>', max_length=80, unique=True, validators=[django.core.validators.MinLengthValidator(4)], verbose_name='video slug'),
        ),
    ]
