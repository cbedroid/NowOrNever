from django import forms
from django.contrib import admin
from image_cropping import ImageCroppingMixin
from django.conf.locale.es import formats as es_formats
from django.utils.html import format_html
from django.utils.html import mark_safe
from .music_models import Artist, Album, Song
from .forms import VideoForm
from .models import Video, Producer, Article, Image, Event, SocialMedia


es_formats.DATETIME_FORMAT = "d M Y H:i:s"


class DateCreateAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )


class ThumbnailAdmin(DateCreateAdmin):
    # readonly_fields = ('thumbnail',)
    form = VideoForm

    def image_tag(self, obj):
        return mark_safe(obj.thumbnail)

    image_tag.short_description = "thumbnail"
    list_display = [
        "title",
        "image_tag",
        "is_featured",
    ]


class SlugFieldAdmin(DateCreateAdmin):
    readonly_fields = ("slug",)


# Register your models here.
admin.site.register(Artist, DateCreateAdmin)
admin.site.register(Album, DateCreateAdmin)
admin.site.register(Song, DateCreateAdmin)
admin.site.register(Video, ThumbnailAdmin)
admin.site.register(Producer, DateCreateAdmin)
admin.site.register(Event, DateCreateAdmin)
admin.site.register(Article, SlugFieldAdmin)
admin.site.register(SocialMedia, DateCreateAdmin)
admin.site.register(Image, DateCreateAdmin)
