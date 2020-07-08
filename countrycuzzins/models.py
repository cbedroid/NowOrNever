import os
import base64
import traceback
from io import BytesIO
from django.db import models
from django.conf import settings
from django.core.files import File
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from image_cropping import ImageCropField,ImageRatioField

MEDIA_ROOT = "static"+settings.MEDIA_ROOT
# Create your models here.

def toNameSpace(instance,*args,**kwargs):
  return  f"images/{instance.name}.png"


class Image(models.Model):
  ''' Images  Model Class '''
  name = models.CharField(max_length=60, blank=True)
  image = models.ImageField(upload_to=toNameSpace,height_field=None,
                             width_field=None, max_length=None)
  #cropping = ImageRatioField('image', '420x360')
  is_showcase = models.BooleanField(default=False)

  def __str__(self):
    return self.name

  """
   Hooking into  ___init___ save method and changing "image" name
   if  "name"  attritube change
  """
  def save(self, *args, **kwargs):
    self.renameImgPath()
    super(Image, self).save(*args, **kwargs)

  def renameImgPath(self):
    """ change image path name according to Image.name attribute"""
    #NOTE: If changing an image name effects other images with similiar path,
    #      then this function NEED to be refactor so names changes wont effect 
    #       other images 
    print('Name Changed')
    name = self.name
    old_name = os.path.basename(self.image.url)
    print('\nNAME',name)
    print('\nOLD_NAME',old_name)
    try:
      if name not in old_name:
        rel_np_path  = 'images/' + name+'.png' # change img name to new name 
        old_path = os.path.abspath(self.image.path)
        new_path = os.path.join(settings.MEDIA_ROOT,rel_np_path)
        os.rename( old_path,new_path) 
        print('\nREL_PATH',old_path)
        print('\nABS_PATH',new_path)
        print('\IMAGE URL.',self.image.url)
        self.image = rel_np_path
    except Exception as e:
      print('\nE',e)
      traceback.print_exc()


  def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


  def img64(self): 
    """Convert  images to base64 data """ 
    try:
      with open('static/' + self.image.url,'rb') as f: 
        data = f.read()
        img = base64.encodebytes(data)
        return f"data:image/jpeg;base64,{str(img.decode('utf8'))}"
    except Exception as error:
      print('\nERROR',error)
      return ""




#           ************************* 
#           ******   CLEAN UP *******
#           ************************* 

@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
  """
  Deletes file from filesystem
  when corresponding `MediaFile` object is deleted.
  """
  if instance.image:
    if os.path.isfile(instance.image.path):
      os.remove(instance.image.path)