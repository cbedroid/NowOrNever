"""
This file will contain all of the artists of country cuzzins.
all models will be derived from countrycuzzins models.py.

Artist models 
"""
from django.db import models
from django.core.validators import MinLengthValidator
from .models import Article, Image, Song


class Artist(models.Model):
  name = models.CharField(max_length=80, blank=True, unique=True)
  profile_image = models.OneToOneField(Image, default='images/no_image_artist.png', on_delete=models.SET_DEFAULT)
  article = models.ManyToManyField(Article, verbose_name='article(s)',
                               blank=True, null=True,
                               )
  created = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated = models.DateTimeField(auto_now=True, auto_now_add=False)

  
  def __str__(self):
    return self.name





class Album(models.Model):

    name = models.CharField(max_length=100, blank=True, unique=True)
    image = models.ForeignKey('Image', related_name='album_image', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=80, unique=True,
                            blank=False, null=False,
                            help_text='<p style="color:red; font-weight:700;"> DO NOT ADD DASHES</p>',
                            validators=[MinLengthValidator(4)]
                            ),
    songs = models.ManyToManyField(Song, verbose_name="list of songs",
                            help_text='<p style="color:#000; font-weight:700;"> Select ALL songs that will be on album</p>',
                            blank=True
                                )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
      return self.name

    def clean(self, *args, **kwargs):
      # Force Album to have at least one song 
      # and less than 20
      MAX_SONGS = 20
      MIN_SONGS = 1

      if MIN_SONGS > self.songs.count() > MAX_SONGS:
          raise ValidationError(f"Album must have at least one ({MIN_SONG}) song and no more than {MAX_SONG}")
      super(ALbum, self).clean(*args, **kwargs)



  
  
