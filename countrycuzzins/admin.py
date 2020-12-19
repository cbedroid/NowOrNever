from django import forms
from django.contrib import admin
from django.conf.locale.es import formats as es_formats
from django.utils.html import mark_safe
from .music_models import Artist, Album, Song
from .forms import VideoForm
from .models import Video, Producer, Image, Event, SocialMedia


es_formats.DATETIME_FORMAT = "d M Y H:i:s"



class DateCreateAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )

class ThumbnailWidget(DateCreateAdmin):
    def image_tag(self, obj):
        try:
            return mark_safe(obj.thumbnail)
        except: 
            return mark_safe(obj.image)

    def image_widget(self, obj):
        return mark_safe(
            '<img class="img-thumbnail ml-1" src={obj.thumbnail.url} style="width:25px;hieght:25px;"></img>'
        )

    image_tag.short_description = "thumbnail"

 
class VideoAdmin(ThumbnailWidget):
    form = VideoForm
    list_display = [
        "title",
        "image_widget",
        "is_featured",
    ]


class SongAdmin(DateCreateAdmin):
    filter_horizontal = ['artist', 'feature_artist']

    def miniplayer(self, obj):
        return mark_safe(
            f'<audio src={obj.audio.url} controls><audio>'
            )

    def artistname(self, obj):
        return obj.get_artists

    def view_count(self, obj):
        return obj.played_count

    view_count.short_description = "views"
    artistname.short_description = "artist(s)"
    miniplayer.short_description = "audio"
    list_display = [
        "name",
        "artistname",
        'view_count',
        "miniplayer",
    ]


# class ImageInline(admin.StackedInline):
#     model = Artist

# @admin.register(Image)
# class ArtistStacked( admin.ModelAdmin):
#     inlines = [ImageInline]


class AlbumAdmin(DateCreateAdmin):
    filter_horizontal = ['songs']


# Register your models here.
admin.site.register(Artist, DateCreateAdmin)
admin.site.register(Image, DateCreateAdmin)
admin.site.register(Producer, DateCreateAdmin)
admin.site.register(Event, DateCreateAdmin)
admin.site.register(SocialMedia, DateCreateAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
