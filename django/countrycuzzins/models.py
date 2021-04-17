from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from core.models import Rating
from django.utils.translation import gettext_lazy as _
from simple_history import register


class Image(models.Model):
    name = models.CharField(max_length=60, blank=False, unique=True)
    image = models.ImageField( upload_to="media/images/" )

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=80, blank=False, unique=True)
    company = models.CharField(max_length=120, blank=True)
    link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    """ Video Model Class """
    title = models.CharField(max_length=100 ,null=True)
    url = models.URLField(max_length=300, null=True)
    short_description = models.CharField(max_length=100, blank=True, null=True)
    long_description = models.TextField(max_length=600, blank=True, null=True)
    producer = models.ForeignKey( Producer, verbose_name="video producer",
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    slug = models.SlugField( verbose_name="video slug", max_length=120, editable=False,)
    rating = models.ManyToManyField( Rating,  blank=True,)
    is_featured = models.BooleanField(
        default=False,
        help_text=_("special video that will be highlighted and featured on website")
    )
    is_youtube = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.slug}'


class Event(models.Model):
    name = models.CharField(
        verbose_name="Event name", max_length=200,
        blank=False, null=True, unique=False
    )
    location = models.CharField(
        max_length=100, 
         unique=False,
        help_text=_("Example: Jackson MS colosseum or Facebook live",)
    )
    event_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.name} | {self.location}  | {self.event_date.strftime("%A, %b %d %Y @ %I:%M %p EST")}'


class SocialMedia(models.Model):
    ''' Social media site for all website platform'''
    name = models.CharField(
        verbose_name="social media site name",
        max_length=100, blank=False,
        null=False, unique=True,
    )
    link = models.CharField(max_length=250, blank=False, null=True)

    def __str__(self):
        return self.name


# ********************************#
# ---TRACK CHANGES IN MODELS --- #
# ********************************#
register(Image)
register(Producer)
register(Video)
register(Event)
register(SocialMedia)

