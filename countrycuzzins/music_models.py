"""
This file will contain all of the artists of country cuzzins.
all models will be derived from countrycuzzins models.py.

Artist models 
"""
from django.db import models
from django.core.validators import MinLengthValidator
from .models import Article, Image, Song
from .utils import add_SlugField


class Artist(models.Model):
  name = models.CharField(max_length=80, blank=True, unique=True)
  profile_image = models.OneToOneField(Image, default='images/no_image_artist.png', on_delete=models.SET_DEFAULT)
  article = models.ManyToManyField(Article, verbose_name='article(s)')
  created = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated = models.DateTimeField(auto_now=True, auto_now_add=False)

  
  def __str__(self):
    return self.name



class Album(models.Model):
    id = models.AutoField(primary_key=True,null=False,blank=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    #name2 = models.CharField(max_length=100, blank=False, null=True,unique=False)
    image = models.ForeignKey('Image', related_name='album_image', on_delete=models.DO_NOTHING)
    slug = models.SlugField(verbose_name="album url",max_length=80, unique=True,
                            blank=False, null=False,
                            help_text='<p style="color:red; font-weight:700;"> DO NOT ADD DASHES</p>',
                            validators=[MinLengthValidator(4)]
                            )
    songs = models.ManyToManyField(Song, verbose_name="list of songs",
                           help_text='<p style="color:#000; font-weight:700;"> Select ALL songs that will be on album</p>',
                             )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
      return self.name

    def save(self, *args, **kwargs):
      self = add_SlugField(self,[self.name,self.id])
      super(Album, self).save(*args, **kwargs)


    def clean(self, *args, **kwargs):
      # Force Album to have at least one song 
      # and less than 20
      MAX_SONGS = 20
      MIN_SONGS = 1

      if MIN_SONGS > self.songs.count() > MAX_SONGS:
          raise ValidationError(f"Album must have at least one ({MIN_SONG}) song and no more than {MAX_SONG}")
      super(Album, self).clean(*args, **kwargs)

    @property
    def songslist(self):
      return list(self.songs.all())




  
  
