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
from core.utils.utils_models import Command, OverwriteStorage, generateSlug


MEDIA_ROOT = "static" + settings.MEDIA_ROOT
help_html_string = """
    Url for this article (basically just a name)</br><br/>
    <div style="color:#000;font-size:14px;">
    ( <span style="color:green;font-weight:700;">
      Example</span>:&nbsp;'Now or Never picture' )</div>
  """


def makeSongName(instance, *args, **kwargs):
    """ Updates song's file name to same name as model's namefield

   Args:
      instance (models.Model): instance of model class

  Returns:
      str: song's MEDIAROOT path name 
  """

    # NOTE: This oly fires on creation of model NOT on every save
    # *** TODO: Put this method in Model's save method to save on every save
    abspath = kwargs.get("abspath", False)
    if abspath:
        return "{}/audio/{}.mp3".format(MEDIA_ROOT, instance.name)

    return "audio/{}.mp3".format(instance.name)


def toNameSpace(instance, *args, **kwargs):
    """ Alter models's FileField path name to models' name field

  Args:
      instance (models.Model): models.Model instance 

  Returns:
      str: abspath file path 
  """
    # Force all images to be PNG file #
    instance_hash = hash(instance.__class__)

    # optional kwargs if model does NOT have an name attribute
    name = kwargs.get("name", None)

    Image_hash = hash(Image)
    Song_hash = hash(Song)
    attr, path, ext = {
        Image_hash: ["image.url", "images/", ".png"],
        Song_hash: ["file.url", "audio/", ".mp3"],
    }.get(instance_hash)

    attr_name = "".join((instance.name, ext))
    setattr(instance, attr, attr_name)

    new_name = f"{path}{instance.name}{ext}"
    return new_name


class Image(models.Model):
    """ Images  Model Class """

    name = models.CharField(max_length=60, blank=True, unique=True)
    image = models.ImageField(
        upload_to=toNameSpace, blank=True, storage=OverwriteStorage()
    )
    is_article = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Hooking into  ___init___ save method and changing "image" name. """

        super(Image, self).save(*args, **kwargs)
        path = pathFromName(self, self.image)
        self.imageResize(path)

    @staticmethod
    def imageResize(imagepath):

        # NOTE: Image resize will run on save function after renameImgPath has
        try:
            DIMENSION = (1500, 800)  # 1500x800/width x height
            if not imagepath:
                return

            img = PIL_IMAGE.open(imagepath)
            img = img.resize(DIMENSION)
            img.save(path)
        except Exception as e:
            print("\nIMAGE_RESIZE ERROR", e)

        def validate_image(fieldfile_obj):
            filesize = fieldfile_obj.file.size
            megabyte_limit = 5.0
            if filesize > megabyte_limit * 1024 * 1024:
                raise ValidationError(
                    "Max file size is %sMB" % str(megabyte_limit))


class Article(models.Model):
    name = models.CharField(max_length=60, unique=True)
    headline = models.CharField(max_length=60, null=True)
    image = models.OneToOneField(
        Image,
        blank=True,
        default="images/no_content.png",
        on_delete=models.SET_DEFAULT,
        primary_key=True,
    )
    blog = models.TextField(max_length=200, null=False)
    slug = models.SlugField(
        verbose_name="article url",
        max_length=80,
        unique=True,
        blank=False,
        null=False,
        help_text='<span id="myslughelp"></span>',
        validators=[MinLengthValidator(4)],
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"Article {self.name}"

    def add_SlugField(self):
        """Create custom url for SlugField from article name on initilization"""

        # NOTE:: MAKE TIS METHOD DYNAMIC FOR ALL MODELS WITH SLUG FIELD
        self.slug = re.sub(
            r"[^\w\-]", "_", "_".join((self.name, self.headline)))

    def save(self, *args, **kwargs):
        self.setIsArticle()
        self.add_SlugField()
        generateSlug(self)
        super(Article, self).save(*args, **kwargs)

    def setIsArticle(self):
        """ On initialization, set Image's model is_article attribute to True """
        self.image.is_article = True
        self.image.save()


class Song(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=True)
    artist = models.CharField(
        "artist(s)",
        default="Country Cuzzins",
        max_length=120,
        blank=True,
        null=True,
        help_text='<p style="color:#000; font-weight:700;"> Main Artist(s) Only</p>',
    )
    feature = models.CharField(
        "feature artists(s)",
        max_length=120,
        blank=True,
        null=True,
        help_text='<p style="color:#000; font-weight:700;"> Feature Artist(s) Only </p><span>(optional)</span>',
    )
    name = models.CharField(
        verbose_name="title", max_length=120, blank=False, null=True, unique=True
    )
    slug = models.SlugField(
        max_length=80,
        unique=True,
        blank=False,
        null=False,
        help_text='<p style="color:red; font-weight:700;"> DO NOT ADD DASHES</p>',
        validators=[MinLengthValidator(4)],
    )
    file = models.FileField(
        max_length=120,
        verbose_name="song file",
        upload_to=makeSongName,
        storage=OverwriteStorage(),
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.feature:
            self.feature = f" ft {self.feature.title()} "
        return f'{self.artist}{self.feature or "" } - {self.name}'

    def save(self, *args, **kwargs):
        self.name = re.sub("\s|\W", "_", self.name)
        self.slug = self.slug.lower().strip()
        super(Song, self).save(*args, **kwargs)
        path = pathFromName(self, self.file)


class Producer(models.Model):
    name = models.CharField(max_length=80, blank=True, unique=True)
    company = models.CharField(max_length=120, blank=True,)
    link = models.URLField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class Video(models.Model):
    """ Video Model Class """

    THUMBNAIL_CHOICES = [(0, 1), (1, 2), (2, 3), (3, 4)]
    _vid_id = None

    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=300, blank=True, null=True)
    thumbnail_choice = models.IntegerField(
        verbose_name="choose a thumbnail", choices=THUMBNAIL_CHOICES, default=1
    )
    thumbnail = models.CharField(max_length=200, blank=True, null=True)
    short_description = models.CharField(max_length=100, blank=True, null=True)
    long_description = models.TextField(max_length=600, blank=True, null=True)
    producer = models.ForeignKey(
        Producer, verbose_name="video producer", on_delete=models.DO_NOTHING
    )

    is_youtube = models.BooleanField(default=False)
    is_music = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="special video that will be highlighted feature on website",
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        managed = True

    @property
    def vid_id(self):
        if hasattr(self, "_vid_id"):
            return self._vid_id
        try:
            return re.match(r".*v\=(\w*)", self.url).group(1)
        except:
            return re.match(r".*/(\w*)", self.url).group(1)

    @vid_id.setter
    def vid_id(self, val):
        # TODO: force constrains on value range
        self.__vid_id = val

    def save(self, *args, **kwargs):
        url = re.sub(r"\.", "", self.url)
        # Convert youtube's video url to embed url
        if "youtube" in url:
            self.is_youtube = True
            # change the url to youtube embed format
            endpoint = re.match(r".*/(\w*)", self.url)
            if not endpoint:
                self.is_youtube = False
                return

            vid_id = endpoint.group(1)
            self._vid_id = vid_id
            # create the embed url
            self.url = f"https://www.youtube.com/embed/{vid_id}"

        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):

    name = models.CharField(
        verbose_name="Event name", max_length=200, blank=True, null=True, unique=False
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=False,
        help_text="Example: Jackson MS colosseum or Facebook live",
    )
    event_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.name} | {self.location}  | {self.event_date.strftime("%A, %b %d %Y @ %I:%M %p EST")}'


class SocialMedia(models.Model):
    # Social media site for all website platform
    name = models.CharField(
        verbose_name="social media site name",
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )
    link = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


#########################################################
#               *************************               #
#               ****  HELP METHODS   ****               #
#               *************************               #
#########################################################


def pathFromName(instance, obj):
    """Rename file path to model name's attribute
  Args:
      instance (class object): models.Models class instance
      obj (class field):  models.Model class field 
      filetype (str):  media field type
      extention (str, optional): extention to assign to path. Defaults to None.

  Returns:
      str: path to file
  """
    # Capture object classname and set the save path and extention
    Image_hash = hash(Image.image.field)
    Song_hash = hash(Song.file.field)
    save_info = {Image_hash: ["images/", ".png"], Song_hash: ["audio/", ".mp3"], }.get(
        hash(obj.field)
    )

    # Force name constrain on any model using this function
    if not hasattr(instance, "name"):
        return

    # get the name attribute from model

    savepath, ext = save_info
    name_of_obj = instance.name

    # check if the model objects has an url field
    # if not then return the current object untouched
    url = getattr(obj, "url", None)
    if not url or not save_info:
        print("\nPathToNameFailed")
        return

    default_path = os.path.basename(obj.url)
    try:
        # Get the basename  minus the extention of the url
        base_path, extention = os.path.splitext((default_path))

        # Change obj basename to obj name
        if name_of_obj != base_path:

            rel_np_path = (
                savepath + str(name_of_obj) + ext
            )  # change img name to new name
            old_path = os.path.abspath(obj.path)
            new_path = os.path.join(settings.MEDIA_ROOT, rel_np_path)

            try:
                os.rename(old_path, new_path)
            except:
                pass
            return rel_np_path
    except Exception as e:
        print("\nE", e)
        traceback.print_exc()
