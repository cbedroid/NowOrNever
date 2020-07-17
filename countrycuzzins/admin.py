from django.contrib import admin
from image_cropping import ImageCroppingMixin          
from .models import Image,Article,Song
from .music_models import Artist,Album


# class ImageCropAdmin(ImageCroppingMixin,DateCreateAdmin):
#   """" Image Cropping Mixin """
#   pass          

class DateCreateAdmin(admin.ModelAdmin):
  readonly_fields = ('created','updated',)

class SlugFieldAdmin(DateCreateAdmin):
  readonly_fields = ('slug',)


# Register your models here.
admin.site.register(Artist,DateCreateAdmin)
admin.site.register(Album,DateCreateAdmin)
admin.site.register(Image,DateCreateAdmin)
admin.site.register(Article,SlugFieldAdmin)
admin.site.register(Song,DateCreateAdmin)
#admin.site.register(Image, MyModelAdmin)
