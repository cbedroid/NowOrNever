import os
import re
import traceback
from django.db import models
from django.conf import settings
from django.core.files import File
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.files.storage import FileSystemStorage
from image_cropping import ImageCropField, ImageRatioField
from argparse import RawTextHelpFormatter
from django.core.management.base import BaseCommand
from PIL import Image as PIL_IMAGE



MEDIA_ROOT = "static" + settings.MEDIA_ROOT

#lambda instance, obj: "audio/{}.mp3".format(instance.name)
def makeSongName(instance, obj,**kwargs):
  #NOTE: This oly fires on creation of model NOT on every save
  #*** TODO: Put this method in Model's save method to save on every save
  print('\nMakeSongName',instance.name)
  abspath = kwargs.get('abspath',False)
  if abspath:
    print('\nABSPATH',abspath)
    return "{}/audio/{}.mp3".format(MEDIA_ROOT,instance.name)
  print('\nNO ABSPATH',abspath)
  return "audio/{}.mp3".format(instance.name)


class OverwriteStorage(FileSystemStorage):
  
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

def js_slugUrl(instance):
  """
    Hacky way to Build SlugField using ip and/or port of website.
    using javascript instead of python to get url address
  """
  slug_url = instance.slug +";"
  html = "".join(('''<span id="myslughelp"></span><script>
        const full = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
        const myhelp = document.getElementById("myslughelp");
        const data = myhelp.parentElement.innerHTML;
        myhelp.innerHTML = full + /article/''' ,slug_url , 
        '''alert('Custom ranned');
      </script>'''
      ))
  instance._meta.get_field('slug').help_text  = html



def toNameSpace(instance, *args, **kwargs):
    """ Force all images to be PNG file """
    # hashed check memory allocated
    instance_hash = hash(instance.__class__)
    # optional kwargs if model doesnt have an name attribute
    name = kwargs.get('name',None) 

    Image_hash = hash(Image)
    Song_hash = hash(Song)
    attr,path,ext= {Image_hash: ['image.url','images/', '.png'],
                 Song_hash: ['file.url','audio/', '.mp3'],
                 }.get(instance_hash)

    attr_name = "".join((instance.name,ext))
    print('\nNP ATTRNAME:',attr_name)
    setattr(instance,attr, attr_name)
    print('\nNP INSTANCE:',instance)
    #print(f"\n\nNP From instance: {instance.file.url}\n")
    # NOTE:: If image does populate with extention
    # then add the extention to path below (save_info[1])
    new_name = f"{path}{instance.name}{ext}"
    print('\nNP NEW_NAME',new_name)
    return new_name

class Command(BaseCommand):
    """ pre-parser hook to change HTML text before rendering to admin """

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

# Create your models here.

class Image(models.Model):
    ''' Images  Model Class '''
    name = models.CharField(max_length=60, blank=True, unique=True)
    image = models.ImageField(upload_to=toNameSpace, blank=True, storage=OverwriteStorage())
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
        super(Image, self).save(*args, **kwargs)
        path = pathToName(self, self.image)
        self.imageResize(path)

    @staticmethod
    def imageResize(imagepath):
        # NOTE: Image resize will run on save function after renameImgPath has
        # set the image path
        try:
            DIMENSION = (1500, 800)  # 1500x800/width x height
            if not imagepath:
                return

            #path = os.path.join(MEDIA_ROOT,path)
            # if not os.path.exists(path):
            #   raise FileNotFoundError(f'Can not resize image! Path "{path}" does not exist')
            img = PIL_IMAGE.open(imagepath)
            img = img.resize(DIMENSION)
            img.save(path)
        except Exception as e:
            print('\nIMAGE_RESIZE ERROR', e)

    def renameImgPath(self):
        """ change image path name according to Image.name attribute"""
        # NOTE: If changing an image name effects other images with similiar path,
        #      then this function NEED to be refactor so names changes wont effect
        #       other images
        name = self.name
        old_name = os.path.basename(self.image.url)
        try:
            re_name = re.search(f'(.*)\.', old_name).group(1)
            if name != re_name:
                rel_np_path = 'images/' + name+'.png'  # change img name to new name
                old_path = os.path.abspath(self.image.path)
                new_path = os.path.join(settings.MEDIA_ROOT, rel_np_path)
                try:
                    os.rename(old_path, new_path)
                except:
                    pass
                self.image = rel_np_path
                return new_path
        except Exception as e:
            print('\nE', e)
            traceback.print_exc()

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" %
                                  str(megabyte_limit))


help_html_string = '''
    Url for this article (basically just a name)</br><br/>
    <div style="color:#000;font-size:14px;">
    ( <span style="color:green;font-weight:700;">
      Example</span>:&nbsp;'Now or Never picture' )</div>
  '''


class Article(models.Model):
    #image = models.ForeignKey('Image', related_name='showcase_image', on_delete=models.CASCADE)
    name = models.CharField(max_length=60, unique=True)
    headline = models.CharField(max_length=60, null=True)
    image = models.OneToOneField(Image, blank=True, default='images/no_content.png', 
                                on_delete=models.SET_DEFAULT, primary_key=True
                                )
    blog = models.TextField(max_length=200, null=False)
    slug = models.SlugField(verbose_name="article url",max_length=80, unique=True,
                            blank=False, null=False,
                            help_text= '<span id="myslughelp"></span>',
                            validators=[MinLengthValidator(4)]
                            )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"Article {self.name}"

    ##NOTE:: MAKE THIS DYNAMIC FOR ALL MODELS 
    def add_SlugField(self): 
        """
          Create custom url for SlugField from article name on initilization
        """
        self.slug = re.sub(r'[^\w\-]','_', "_".join((self.name,self.headline)))
        print('\nSELF.SLUG',self.slug)

    def save(self, *args, **kwargs):
        self.setIsArticle()
        self.add_SlugField()
        js_slugUrl(self)
        super(Article, self).save(*args, **kwargs)

    def setIsArticle(self):
        """ On initialization, set Image's model is_article attribute to True """
        self.image.is_article = True
        self.image.save()


class Song(models.Model):
    # NOTE: Check out models.FieldPath to specify the directory for song
    # this may need to be force on albums (child class) since we will have
    # more than one album as the projects grows larger
    # https://docs.djangoproject.com/en/3.0/ref/models/fields/
    id = models.AutoField(primary_key=True,null=False,blank=True)
    artist = models.CharField('artist(s)', default="Country Cuzzins",
                              max_length=120, blank=True, null=True,
                              help_text='<p style="color:#000; font-weight:700;"> Main Artist(s) Only</p>'
                              )
    feature = models.CharField('feature artists(s)',
                               max_length=120, blank=True, null=True,
                               help_text='<p style="color:#000; font-weight:700;"> Feature Artist(s) Only </p><span>(optional)</span>',
                               )

    name = models.CharField( verbose_name = "title",
        max_length=120, blank=False, null=True, unique=True)
    slug = models.SlugField(max_length=80, unique=True,
                            blank=False, null=False,
                            help_text='<p style="color:red; font-weight:700;"> DO NOT ADD DASHES</p>',
                            validators=[MinLengthValidator(4)]
                            )
    file = models.FileField(max_length=120,verbose_name="song file",upload_to=makeSongName,
      storage=OverwriteStorage()
        )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.feature:
            self.feature = f" ft {self.feature.title()} "
        return f'{self.artist}{self.feature or "" } - {self.name}'

    def save(self, *args, **kwargs):
        self.name = re.sub('\s|\W','_',self.name)
        self.slug = self.slug.lower().strip()
        #self.file = makeSongName(self,self.name,abspath=True)
        super(Song, self).save(*args, **kwargs)
        path = pathToName(self, self.file)
        print('\nSELF.FILE.URL',path)


class Video(models.Model):
  ''' Video Model Class '''
  name = models.CharField(max_length=100, blank=True, null=True)
  url = models.URLField(max_length=300, blank=True,null=True)
  is_music = models.BooleanField(default=true)

  
  def __str__(self):
      return self.__class__.name__
  

#########################################################
#               *************************               #
#               ****  HELP METHODS   ****               #
#               *************************               #
#########################################################


def pathToName(instance, obj):
    #def inner
      """Rename file path to model name's attribute
      Args:
          instance (class object): models.Models class instance
          obj (class field):  models.Model class field 
          filetype (str):  media field type
          extention (str, optional): extention to assign to path. Defaults to None.

      Returns:
          str: path to file
      """
      # capture object classname and set
      # the save path and extention
      Image_hash = hash(Image.image.field)
      Song_hash = hash(Song.file.field)
      save_info = {Image_hash: ['images/', '.png'],
                  Song_hash: ['audio/', '.mp3'],
                  }.get(hash(obj.field))

      # Force name constrain on any model using this function
      if not hasattr(instance, "name"):
          return

      # get the name attribute from model

      savepath,ext = save_info
      name_of_obj = instance.name

      # check if the model objects has an url field
      # if not then return the current object untouched
      url = getattr(obj, 'url', None)
      if not url or not save_info:
          print('\nPathToNameFailed')
          return

      default_path = os.path.basename(obj.url)
      try:
          # get the basename  minus the extention of the url
          base_path, extention = os.path.splitext((default_path))
          #base_path = re.search(f'(.*)\.', default_path).group(1)

          # change obj basename to obj name
          if name_of_obj != base_path:
              rel_np_path = savepath + str(name_of_obj) +  ext # change img name to new name
              print('\nREL_NP_PATH',rel_np_path)
              old_path = os.path.abspath(obj.path)
              new_path = os.path.join(settings.MEDIA_ROOT, rel_np_path)
              print('\nOLD_PATH',old_path)
              print('\nNEW_PATH',new_path)
              try:
                  os.rename(old_path, new_path)
              except:
                  pass

              #obj = rel_np_path
              print('\n\nRETURN GOOD\n')
              print('------------------------------------------------\n')
              return rel_np_path
      except Exception as e:
          print('\nE', e)
          traceback.print_exc()





#########################################################
#           *************************                   #
#           ******   CLEAN UP *******                   #
#           *************************                   #
#########################################################

@receiver(models.signals.post_delete, sender=Image)
@receiver(models.signals.post_delete, sender=Song)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    try:
      if instance.image:
          if os.path.isfile(instance.image.path):
              os.remove(instance.image.path)
    except:
      if instance.file:
        if os.path.isfile(instance.file.path):
              os.remove(instance.file.path)


ART = Article
IMG = Image