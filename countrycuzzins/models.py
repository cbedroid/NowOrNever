import os
import re
import traceback
from django.db import models
from django.conf import settings
from django.core.files import File
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from image_cropping import ImageCropField,ImageRatioField
from argparse import RawTextHelpFormatter
from django.core.management.base import BaseCommand
from PIL import Image as PIL_IMAGE


MEDIA_ROOT = "static"+settings.MEDIA_ROOT

def toNameSpace(instance,*args,**kwargs):
  path = f"images/{instance.name}.png"
  return path



class Command(BaseCommand):
  """ pre-parser hook to change HTML text before rendering to admin """
  def create_parser(self, *args, **kwargs):
    parser = super(Command, self).create_parser(*args, **kwargs)
    parser.formatter_class = RawTextHelpFormatter
    return parser

# Create your models here.
class Image(models.Model):
  ''' Images  Model Class '''
  name = models.CharField(max_length=60, blank=True,unique=True)
  image = models.ImageField(upload_to=toNameSpace,blank=True)
  #cropping = ImageRatioField('image', '420x360')
  is_article = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated = models.DateTimeField(auto_now=True, auto_now_add=False)

  def __str__(self):
    return self.name

  """
   Hooking into  ___init___ save method and changing "image" name
   if  "name"  attritube change
  """
  def save(self, *args, **kwargs):
    path = self.renameImgPath()
    self.imageResize(path)
    super(Image, self).save(*args, **kwargs)

  @staticmethod
  def imageResize(imagepath):
    #NOTE: Image resize will run on save function after renameImgPath has 
    # set the image path  
    try:
      DIMENSION = (1500,800) # 1500x800/width x height
      if not imagepath:
        print('\nNO IMAGEPATH TO RESIZE')
        return 

      #path = os.path.join(MEDIA_ROOT,path)
      # if not os.path.exists(path):
      #   raise FileNotFoundError(f'Can not resize image! Path "{path}" does not exist')
      img = PIL_IMAGE.open(imagepath)
      img = img.resize(DIMENSION)
      img.save(path)
      print('\nIMAGE SAVED:',imagepath)
    except Exception as e:
      print('\nIMAGE_RESIZE ERROR',e)

  def renameImgPath(self):
    """ change image path name according to Image.name attribute"""
    #NOTE: If changing an image name effects other images with similiar path,
    #      then this function NEED to be refactor so names changes wont effect 
    #       other images 
    # print('Name Changed')
    name = self.name
    old_name = os.path.basename(self.image.url)
    # print('\nNAME',name)
    # print('\nOLD_NAME',old_name)
    try:
      re_name = re.search(f'(.*)\.',old_name).group(1)
      # print('\nRE_NAME',re_name)
      if name !=  re_name:
        rel_np_path  = 'images/' + name+'.png' # change img name to new name 
        old_path = os.path.abspath(self.image.path)
        new_path = os.path.join(settings.MEDIA_ROOT,rel_np_path)
        try:
          os.rename( old_path,new_path) 
        except: 
          pass
        # print('\nREL_PATH',old_path)
        # print('\nABS_PATH',new_path)
        # print('\IMAGE URL.',self.image.url)
        self.image = rel_np_path
        print('\nNEW_PATH',new_path)
        return new_path
    except Exception as e:
      print('\nE',e)
      traceback.print_exc()
  


  def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
        


help_html_string = '''Url for this article (basically just a name)</br><br/>
                       <div style="color:#000;font-size:14px;">
                        ( <span style="color:green;font-weight:700;">
                          Example</span>:&nbsp;'Now or Never picture' )</div>
                     '''
class Article(models.Model):
  #image = models.ForeignKey('Image', related_name='showcase_image', on_delete=models.CASCADE)
  slug = models.SlugField(max_length=80,unique=True,
        blank=False,null=False,
        help_text=help_html_string,
        validators=[MinLengthValidator(4)]
        )
  image = models.OneToOneField(Image,default=1,on_delete=models.SET_DEFAULT, primary_key=True)
  headline = models.CharField(max_length=60, blank=True, null=True)
  blog  = models.TextField(max_length=200,blank=True,null=False)
  created = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated = models.DateTimeField(auto_now=True, auto_now_add=False)


  def __str__(self):
    return f"Article {self.slug}"

  def save(self, *args, **kwargs):
    self.setIsArticle()
    super(Article, self).save(*args, **kwargs)

  def setIsArticle(self):
    """ On initialization, set Image's model is_article attribute to True """
    self.image.is_article  = True
    self.image.save()



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
