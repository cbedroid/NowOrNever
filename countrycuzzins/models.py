import re
from django.db import models
from django.core.validators import MinLengthValidator
from core.utils.utils_models import Command, OverwriteStorage, generateSlug
from core.models import Rating


class Image(models.Model):
    """ Images  Model Class """

    name = models.CharField(max_length=60, blank=True, unique=True)
    image = models.ImageField(
        upload_to="images", blank=True,
        storage=OverwriteStorage()
    )
    is_article = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Hooking into  ___init___ save method and changing "image" name. """
        super().save(*args, **kwargs)


class Article(models.Model):
    name = models.CharField(max_length=60, unique=True)
    headline = models.CharField(max_length=60, null=True)
    image = models.OneToOneField(
        Image, default="images/no_content.png",
        blank=True, primary_key=True,
        on_delete=models.SET_DEFAULT
    )
    blog = models.TextField(max_length=200, null=False)
    slug = models.SlugField(
        verbose_name="article url",
        max_length=80,
        unique=True, blank=False, null=False,
        help_text='<span id="myslughelp"></span>',
        validators=[MinLengthValidator(4)],
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"Article {self.name}"

    def save(self, *args, **kwargs):
        self.setIsArticle()
        generateSlug(self)
        super(Article, self).save(*args, **kwargs)

    def setIsArticle(self):
        """ On initialization, set Image's model is_article attribute to True """
        self.image.is_article = True
        self.image.save()


class Producer(models.Model):
    name = models.CharField(max_length=80, blank=True, unique=True)
    company = models.CharField(max_length=120, blank=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class Video(models.Model):
    """ Video Model Class """
    THUMBNAIL_CHOICES = [(0, 1), (1, 2), (2, 3), (3, 4)]

    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=300, blank=True, null=True)
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
        on_delete=models.DO_NOTHING,
    )
    slug = models.SlugField(
        verbose_name="video slug",
        max_length=80,
        unique=True, blank=False, null=False,
        help_text='<span id="myslughelp"></span>',
        validators=[MinLengthValidator(4)],
    )
    rating = models.ManyToManyField(
        Rating, related_name="video_ratings", blank=True
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="special video that will be highlighted feature on website"
    )
    is_youtube = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        managed = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):
    name = models.CharField(
        verbose_name="Event name", max_length=200,
        blank=True, null=True, unique=False
    )
    location = models.CharField(
        max_length=100, blank=True,
        null=True, unique=False,
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
        max_length=100, blank=True,
        null=True, unique=True,
    )
    link = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name
