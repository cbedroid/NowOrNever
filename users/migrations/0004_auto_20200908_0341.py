# Generated by Django 3.0.7 on 2020-09-08 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_likes_rating"),
    ]

    operations = [
        migrations.DeleteModel(name="Likes",),
        migrations.DeleteModel(name="Rating",),
    ]
