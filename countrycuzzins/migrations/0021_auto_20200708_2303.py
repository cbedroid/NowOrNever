# Generated by Django 3.0.7 on 2020-07-09 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countrycuzzins', '0020_remove_image_cropping'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='is_showcase',
            new_name='is_article',
        ),
    ]
