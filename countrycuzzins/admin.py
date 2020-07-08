from django.contrib import admin
from image_cropping import ImageCroppingMixin          
from .models import Image

#class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):          
#  pass          

# Register your models here.
admin.site.register(Image)
#admin.site.register(Image, MyModelAdmin)
