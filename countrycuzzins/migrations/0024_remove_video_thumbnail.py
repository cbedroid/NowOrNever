# Generated by Django 3.0.7 on 2020-09-08 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("countrycuzzins", "0023_auto_20200908_0550"),
    ]

    operations = [
        migrations.RemoveField(model_name="video", name="thumbnail",),
    ]
