# Generated by Django 3.0.7 on 2020-09-08 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("countrycuzzins", "0021_auto_20200908_0538"),
    ]

    operations = [
        migrations.RenameField(model_name="video", old_name="name", new_name="title",),
    ]
