# Generated by Django 3.0.7 on 2020-07-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0049_auto_20200723_0256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='id',
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(default=1, max_length=120, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
    ]