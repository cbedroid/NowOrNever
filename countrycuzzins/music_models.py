"""
This file will contain all of the artists of country cuzzins.
all models will be derived from countrycuzzins models.py.

Artist models 
"""
import os
import traceback
from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from .models import Image
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.dispatch import Signal
from core.utils.utils_models import (
    Command,
    OverwriteStorage,
    generateSlug,
    urlParseSlugField,
)

MEDIA_ROOT = "static" + settings.MEDIA_ROOT


def makeSongName(instance, *args, **kwargs):
    """Updates song's file name to same name as model's namefield

     Args:
        instance (models.Model): instance of model class

    Returns:
        str: song's MEDIAROOT path name
    """

    # NOTE: This oly fires on creation of model NOT on every save
    # *** TODO: Put this method in Model's save method to save on every save
    abspath = kwargs.get("abspath", False)
    if abspath:
        return "{}/audio/{}.mp3".format(MEDIA_ROOT, instance.name)
    return "audio/{}.mp3".format(instance.name)


class Artist(models.Model):
    name = models.CharField(max_length=80, blank=True, unique=True)
    image = models.ForeignKey(Image, default=1, on_delete=models.SET_DEFAULT)
    bio = models.TextField(max_length=500, default="Country Cuzzins Artist")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class Song(models.Model):
    _song_signal = Signal()

    artist = models.ManyToManyField(
        Artist, related_name="main_artist", blank=True, null=True)
    feature_artist = models.ManyToManyField(
        Artist,
        verbose_name="feature artists(s)",
        related_name="featured_artist",
        blank=True,
        null=True,
        help_text='<p style="color:#000; font-weight:700;"> Feature Artist(s) Only </p><span>(optional)</span>',
        )
    name = models.CharField(
        verbose_name="title",
        max_length=120,
        blank=False,
        null=True,
        unique=True
        )
    audio = models.FileField(
        max_length=120,
        upload_to=makeSongName,
        storage=OverwriteStorage(),
        )
    played_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(
        max_length=150,
        default="",
        editable=False,
        validators=[MinLengthValidator(4)],
    )

    def save(self, *args, **kwargs):
        slug_name = self.name
        self.slug = slugify(slug_name)
        super().save(*args, **kwargs)

    @property
    def get_artists(self):
        main_artists = " & ".join(
            [artist.name for artist in self.artist.get_queryset()])
        featured_artists = " & ".join(
            [artist.name for artist in self.feature_artist.get_queryset()]
            )
        if featured_artists:
            return " ft ".join((main_artists, featured_artist))
        return main_artists

    @property
    def get_playcount_url(self, *args, **kwargs):
        return reverse('country_cuzzins:song-playcount',
            kwargs={'pk': self.pk, }
            )

    def __str__(self):
        return f'{self.name} - {self.get_artists}'


class Album(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    cover = models.ForeignKey(
        Image,
        related_name="album_cover",
        null=True,
        default=1,
        on_delete=models.DO_NOTHING,
    )
    songs = models.ManyToManyField(Song, related_name="songs")
    description = models.TextField(max_length=1000, blank=True,null=True,help_text='<div style="color:red"> HTML SAFE</div>')
    is_featured = models.BooleanField(
        default=False, help_text="Do you want this on the home page")
    slug = models.SlugField(
        max_length=150,
        default="",
        editable=False,
        validators=[MinLengthValidator(4)],
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug_name = self.name
        self.slug = slugify(slug_name)
        super().save(*args, **kwargs)

    @property
    def songslist(self):
        return self.songs.get_queryset()

    @property
    def get_absolute_url(self):
        return reverse('country_cuzzins:album-detail',
            kwargs={
                'slug': self.slug,
            })
