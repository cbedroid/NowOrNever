# Generated by Django 3.2 on 2021-04-17 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactus',
            name='ip_address',
        ),
    ]
