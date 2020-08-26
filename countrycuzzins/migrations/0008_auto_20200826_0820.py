# Generated by Django 3.0.7 on 2020-08-26 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0007_auto_20200826_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ForeignKey(blank=True, default='images/default_album.png', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='album_image', to='countrycuzzins.Image'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='profile_image',
            field=models.OneToOneField(default='images/default_artist.png', on_delete=django.db.models.deletion.SET_DEFAULT, to='countrycuzzins.Image'),
        ),
    ]
