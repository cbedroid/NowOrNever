"""
This file will contain all of the artists of country cuzzins.
all models will be derived from countrycuzzins models.py.

Artist models 
"""
from models import *

class Artist(models.Model)
  #profile_image = models.OneToOne('Image', related_name='image', on_delete=models.CASCADE)
  profile_image = models.OneToOneField(Image,default=1,on_delete=models.SET_DEFAULT)
  articles = models.ManyToManyField(Article)
  

class Album(mmodels.Model):
  pass
