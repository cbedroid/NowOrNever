from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from core.utils.utils_models import Command, OverwriteStorage
from core.models import Rating


class Image(models.Model):
    """ Images  Model Class """
    name = models.CharField(max_length=60, blank=False, unique=True)
    image = models.ImageField(
        upload_to="images", 
        storage=OverwriteStorage()
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Hooking into  ___init___ save method and changing "image" name. """
        super().save(*args, **kwargs)



class Producer(models.Model):
    name = models.CharField(max_length=80, blank=False, unique=True)
    company = models.CharField(max_length=120, blank=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class Video(models.Model):
    """ Video Model Class """
    THUMBNAIL_CHOICES = [(0, 1), (1, 2), (2, 3), (3, 4)]

    title = models.CharField(max_length=100 ,null=True)
    url = models.URLField(max_length=300, null=True)
    # TODO: remove this and put it in admin form, Correct signals if moved
    thumbnail_choice = models.IntegerField(
        verbose_name="choose a thumbnail", choices=THUMBNAIL_CHOICES, default=1
    )
    thumbnail = models.CharField(max_length=200, blank=True, null=True)
    short_description = models.CharField(max_length=100, blank=True, null=True)
    long_description = models.TextField(max_length=600, blank=True, null=True)
    producer = models.ForeignKey(
        Producer, verbose_name="video producer",
        related_name="video_producer",
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    slug = models.SlugField(
        verbose_name="video slug",
        max_length=120,
        editable=False,
        validators=[MinLengthValidator(4)],
    )
    rating = models.ManyToManyField(
        Rating, related_name="video_ratings", blank=True,
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="special video that will be highlighted and featured on website"
    )
    is_youtube = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        slug_name = self.title
        self.slug = slugify(slug_name)
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
        help_text="Example: Jackson MS colosseum or Facebook live",
    )
    event_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

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
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name
