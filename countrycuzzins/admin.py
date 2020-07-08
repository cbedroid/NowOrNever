from django.contrib import admin
from image_cropping import ImageCroppingMixin          
from .models import Image,Article

#class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):          
#  pass          

class DateCreateAdmin(admin.ModelAdmin):
  readonly_fields = ('upload_date',)

# Register your models here.
admin.site.register(Image,DateCreateAdmin)
admin.site.register(Article)
#admin.site.register(Image, MyModelAdmin)
