# Generated by Django 3.0.7 on 2020-07-23 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0041_auto_20200723_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='album_image', to='countrycuzzins.Image'),
        ),
    ]