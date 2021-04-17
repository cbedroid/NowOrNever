from django import forms
from django.contrib import admin
from django.conf.locale.es import formats as es_formats
from django.utils.html import mark_safe
from .music_models import Artist, Album, Song
from .forms import VideoForm
from .models import Video, Producer, Image, Event, SocialMedia


es_formats.DATETIME_FORMAT = "d M Y H:i:s"




class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    list_display = (
        "title",
        "is_featured",
        )


class SongAdmin(admin.ModelAdmin):
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



class AlbumAdmin(admin.ModelAdmin):
    filter_horizontal = ['songs']


# Register your models here.
admin.site.register(Artist)
admin.site.register(Image)
admin.site.register(Producer)
admin.site.register(Event)
admin.site.register(SocialMedia)
admin.site.register(Video, VideoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
