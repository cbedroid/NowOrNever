# Generated by Django 3.0.7 on 2020-07-23 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0038_auto_20200723_0201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='id',
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
