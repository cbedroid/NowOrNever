# Generated by Django 3.0.7 on 2020-12-19 00:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0022_auto_20201218_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(default='', max_length=120, validators=[django.core.validators.MinLengthValidator(4)], verbose_name='video slug'),
        ),
    ]
