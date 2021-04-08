# Generated by Django 3.0.7 on 2020-12-19 08:51

import core.utils.utils_models
import countrycuzzins.music_models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_contactus_has_account'),
        ('countrycuzzins', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={},
        ),
        migrations.RemoveField(
            model_name='album',
            name='image',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='article',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='image',
            name='is_article',
        ),
        migrations.RemoveField(
            model_name='song',
            name='feature',
        ),
        migrations.RemoveField(
            model_name='song',
            name='file',
        ),
        migrations.RemoveField(
            model_name='video',
            name='is_music',
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='album_cover', to='countrycuzzins.Image'),
        ),
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True, help_text='<div style="color:red"> HTML SAFE</div>', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='Do you want this on the home page'),
        ),
        migrations.AddField(
            model_name='artist',
            name='bio',
            field=models.TextField(default='Country Cuzzins Artist', max_length=500),
        ),
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='countrycuzzins.Image'),
        ),
        migrations.AddField(
            model_name='song',
            name='audio',
            field=models.FileField(default=1, max_length=120, storage=core.utils.utils_models.OverwriteStorage(), upload_to=countrycuzzins.music_models.makeSongName),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='feature_artist',
            field=models.ManyToManyField(blank=True, help_text='<p style="color:#000; font-weight:700;"> Feature Artist(s) Only </p><span>(optional)</span>', null=True, related_name='featured_artist', to='countrycuzzins.Artist', verbose_name='feature artists(s)'),
        ),
        migrations.AddField(
            model_name='song',
            name='played_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='slug',
            field=models.SlugField(default=1, editable=False, max_length=120, validators=[django.core.validators.MinLengthValidator(4)], verbose_name='video slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=150, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
        migrations.AlterField(
            model_name='album',
            name='songs',
            field=models.ManyToManyField(related_name='songs', to='countrycuzzins.Song'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(default=1, help_text='Example: Jackson MS colosseum or Facebook live', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Event name'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(storage=core.utils.utils_models.OverwriteStorage(), upload_to='images'),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='link',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='name',
            field=models.CharField(default=1, max_length=100, unique=True, verbose_name='social media site name'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='song',
            name='artist',
        ),
        migrations.AddField(
            model_name='song',
            name='artist',
            field=models.ManyToManyField(related_name='main_artist', to='countrycuzzins.Artist'),
        ),
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=150, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
        migrations.AlterField(
            model_name='video',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='special video that will be highlighted and featured on website'),
        ),
        migrations.AlterField(
            model_name='video',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='video_producer', to='countrycuzzins.Producer', verbose_name='video producer'),
        ),
        migrations.AlterField(
            model_name='video',
            name='rating',
            field=models.ManyToManyField(blank=True, null=True, related_name='video_ratings', to='core.Rating'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(max_length=300, null=True),
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]