# Generated by Django 3.0.7 on 2020-07-23 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0037_auto_20200723_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]