# Generated by Django 3.0.7 on 2020-07-09 01:56

import countrycuzzins.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0018_auto_20200708_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, upload_to=countrycuzzins.models.toNameSpace),
        ),
    ]
