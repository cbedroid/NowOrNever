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
    profile_image = models.OneToOneField(
        Image, default="images/default_artist.png", on_delete=models.SET_DEFAULT
    )
    article = models.ManyToManyField(Article, verbose_name="article(s)")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class Song(models.Model):
    # id = models.AutoField(primary_key=True, null=False, blank=True)
    artist = models.CharField(
        "artist(s)",
        default="Country Cuzzins",
        help_text='<p style="color:#000; font-weight:700;"> Main Artist(s) Only</p>',
        blank=True,
        null=True,
        max_length=120,
    )

    feature = models.CharField(
        "feature artists(s)",
        max_length=120,
        blank=True,
        null=True,
        help_text='<p style="color:#000; font-weight:700;"> Feature Artist(s) Only </p><span>(optional)</span>',
    )
    name = models.CharField(
        verbose_name="title", max_length=120, blank=False, null=True, unique=True
    )
    slug = models.SlugField(
        max_length=80,
        unique=True,
        blank=False,
        null=False,
        help_text='<p style="color:red; font-weight:700;"> DO NOT ADD DASHES</p>',
        validators=[MinLengthValidator(4)],
    )
    file = models.FileField(
        max_length=120,
        verbose_name="song file",
        upload_to=makeSongName,
        storage=OverwriteStorage(),
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.feature:
            self.feature = f" ft {self.feature.title()} "
        return f'{self.artist}{self.feature or "" } - {self.name}'

    def save(self, *args, **kwargs):
        self.name = re.sub("\s|\W", "_", self.name)
        self.slug = self.slug.lower().strip()
        super(Song, self).save(*args, **kwargs)
        path = pathFromName(self, self.file)


class Album(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    image = models.ForeignKey(
        "Image",
        related_name="album_image",
        null=True,
        blank=True,
        default=1,
        on_delete=models.DO_NOTHING,
    )

    slug = models.SlugField(
        verbose_name="album url",
        max_length=80,
        unique=True,
        blank=False,
        null=False,
        help_text='<p style="color:red; font-weight:700;"> DO NOT ADD DASHES</p>',
        validators=[MinLengthValidator(4)],
    )
    songs = models.ManyToManyField(Song, related_name="alum_songs")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            super(Album, self).save(*args, **kwargs)

        self = urlParseSlugField(self, [self.name, self.id])
        super(Album, self).save(*args, **kwargs)

    # def clean(self, *args, **kwargs):
    #     # Force Album to have at least one song
    #     # and less than 20
    #     MAX_SONGS = 20
    #     MIN_SONGS = 1
    #     if MIN_SONGS > self.songs.count() > MAX_SONGS:
    #         raise ValidationError(
    #             f"Album must have at least one ({MIN_SONG}) song and no more than {MAX_SONG}"
    #         )
    #     super(Album, self).clean(*args, **kwargs)

    @property
    def songslist(self):
        # NOTE: Sept 24, songs are now retrieved through Song'srelated_name
        try:
            return self.songs.all()
        except:
            pass

    @property
    def song_urls(self):
        # NOTE:
        #  Sept 24, songs are now retrieved through Song'srelated_name
        try:
            return [song.file.url for song in self.album_songs.all()]
        except:
            pass


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
    Song_hash = hash(Song.file.field)
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
