from django.contrib import admin
from image_cropping import ImageCroppingMixin          
from django.conf.locale.es import formats as es_formats
from .models import Image,Article,Song, Video,SocialMedia,Event
from .music_models import Artist,Album



# class ImageCropAdmin(ImageCroppingMixin,DateCreateAdmin):
#   """" Image Cropping Mixin """
#   pass          


es_formats.DATETIME_FORMAT = "d M Y H:i:s"

class DateCreateAdmin(admin.ModelAdmin):
  readonly_fields = ('created','updated',)

class SlugFieldAdmin(DateCreateAdmin):
  readonly_fields = ('slug',)


# Register your models here.
admin.site.register(Artist,DateCreateAdmin)
admin.site.register(Album,DateCreateAdmin)
admin.site.register(Song,DateCreateAdmin)
admin.site.register(Video,DateCreateAdmin)
admin.site.register(Event, DateCreateAdmin)
admin.site.register(Article,SlugFieldAdmin)
admin.site.register(SocialMedia,DateCreateAdmin)
admin.site.register(Image,DateCreateAdmin)
