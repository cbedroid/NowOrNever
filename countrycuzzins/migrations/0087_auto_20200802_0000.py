# Generated by Django 3.0.7 on 2020-08-02 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0086_auto_20200801_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ForeignKey(blank=True, default='images/_no_image_profile.png', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='album_image', to='countrycuzzins.Image'),
        ),
    ]
