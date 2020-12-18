"""
This file will contain all of the artists of country cuzzins.
all models will be derived from countrycuzzins models.py.

Artist models 
"""
import os
import re
import traceback
from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from .models import Article, Image
from core.utils.utils_models import (
    Command,
    OverwriteStorage,
    generateSlug,
    urlParseSlugField,
)
# new features 
from django.urls import reverse,reverse_lazy
from django.utils.text import slugify
from django.dispatch  import Signal




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
    bio = models.TextField(max_length=500,default="Country Cuzzins Artist")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.name

class Song(models.Model):
    _song_signal = Signal()
    artist = models.ManyToManyField(Artist,related_name="main_artist",blank=True,null=True)
    feature_artist = models.ManyToManyField(
        Artist,
        verbose_name = "feature artists(s)",
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

    slug = models.SlugField(
        max_length=150,
        default="",
        editable=False,
        validators=[MinLengthValidator(4)],
    )
    
    played_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self,*args,**kwargs): 
        slug_name = self.name
        self.slug = slugify(slug_name)
        super().save(*args, **kwargs)

    @property
    def get_artists(self):
        main_artists =  " & ".join([artist.name for artist in self.artist.get_queryset()])
        featured_artists =  " & ".join(
            [artist.name for artist in self.feature_artist.get_queryset()]
            )
        if featured_artists:
            return " ft ".join((main_artists,featured_artist))
        return main_artists

    @property
    def get_playcount_url(self,*args,**kwargs):
        return reverse('country_cuzzins:song-playcount',
            kwargs={
                'pk': self.pk,
            })

    def __str__(self):
        return f'{self.name} - {self.get_artists}'


class Album(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    cover = models.ForeignKey(
        Image,
        related_name="album_cover",
        null=True,
        blank=True,
        default=1,
        on_delete=models.DO_NOTHING,
    )
    songs = models.ManyToManyField(Song, related_name="songs")
    is_featured = models.BooleanField(default=False,help_text="Do you want this on the home page")
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

    def save(self,*args,**kwargs): 
        slug_name = self.name
        self.slug = slugify(slug_name)
        super().save(*args, **kwargs)

    @property
    def songslist(self):
        return self.songs.get_queryset()

    @property
    def get_absolute_url(self):
        return  reverse('country_cuzzins:album-detail',
            kwargs={
                'slug': self.slug,
            })

# ***************************************#
# ***************************************#
# ***************************************#
def pathFromName(instance, obj):
    """Rename file path to model name's attribute
    Args:
        instance (class object): models.Models class instance
        obj (class field):  models.Model class field
        filetype (str):  media field type
        extention (str, optional): extention to assign to path. Defaults to None.

    Returns:
        str: path to file
    """
    # Capture object classname and set the save path and extention
    Song_hash = hash(Song.audio.field)
    save_info = {
        Song_hash: ["audio/", ".mp3"],
    }.get(hash(obj.field))

    # Force name constrain on any model using this function
    if not hasattr(instance, "name"):
        return

    # get the name attribute from model

    savepath, ext = save_info
    name_of_obj = instance.name

    # check if the model objects has an url field
    # if not then return the current object untouched
    url = getattr(obj, "url", None)
    if not url or not save_info:
        print("\nPathToNameFailed")
        return

    default_path = os.path.basename(obj.url)
    try:
        # Get the basename  minus the extention of the url
        base_path, extention = os.path.splitext((default_path))

        # Change obj basename to obj name
        if name_of_obj != base_path:
            rel_np_path = (
                savepath + str(name_of_obj) + ext
            )  # change img name to new name
            old_path = os.path.abspath(obj.path)
            new_path = os.path.join(settings.MEDIA_ROOT, rel_np_path)
            try:
                os.rename(old_path, new_path)
            except:
                pass
            return rel_np_path
    except Exception as e:
        print("\nE", e)
        traceback.print_exc()

