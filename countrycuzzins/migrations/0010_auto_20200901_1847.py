# Generated by Django 3.0.7 on 2020-09-01 22:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("countrycuzzins", "0009_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
