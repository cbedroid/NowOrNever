# Generated by Django 3.0.7 on 2020-07-23 08:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0051_auto_20200723_0402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='id',
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=120, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
    ]