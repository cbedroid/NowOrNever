# Generated by Django 3.0.7 on 2020-12-19 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='has_account',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]