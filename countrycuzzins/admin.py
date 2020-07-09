from django.contrib import admin
from image_cropping import ImageCroppingMixin          
from .models import Image,Article


# class ImageCropAdmin(ImageCroppingMixin,DateCreateAdmin):
#   """" Image Cropping Mixin """
#   pass          

class DateCreateAdmin(admin.ModelAdmin):
  readonly_fields = ('created','updated',)

# Register your models here.
admin.site.register(Image,DateCreateAdmin)
admin.site.register(Article,DateCreateAdmin)
#admin.site.register(Image, MyModelAdmin)
