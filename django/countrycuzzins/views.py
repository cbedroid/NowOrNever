from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from .models import Image,Video,SocialMedia, Event
from .music_models import Album, Song
from django.db.models import Q

# Create your views here.


class HomeView(ListView):
    model = Album
    template_name = "countrycuzzins/index.html"

    def get_context_data(self,*args,**kwargs):
        context = {}
        context.update( {
            "album": Album.objects.filter(Q(is_featured=True) |Q(is_featured=False)).first(),
            "images": Image.objects.all(),
            "music_videos": Video.objects.all(),
            "social_media": SocialMedia,
            "test_image": Image.objects.last(),
        })
        return context

class AlbumDetailView(DetailView):
    model = Album
    template_name = "countrycuzzins/album-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["songs"] = self.object.songs.get_queryset()
        return context


class SongPlayCountView(View):
    model = Song
    response = {'success': False, "data": {}}

    def post(self, *args, **kwargs):
        song_id = self.request.POST.get('pk') or kwargs.get('pk')
        print('SONG_ID', song_id)
        album_songs = Song.objects.all()
        song = album_songs.filter(pk=song_id)
        if song.exists() and album_songs.exists():
            album_song_views = []
            if song:
                song = song.first()
                song.played_count += 1
                self.response.update(dict(data=dict(
                    song=song.name,
                    song_id=song_id,
                    song_count=song.played_count,
                    total_views=sum(x.played_count for x in album_songs)
                    ),
                ))
                song.save()
                self.response['success'] = True
        return JsonResponse(self.response, safe=False)


class EventList(ListView):
    model = Event
    context_object_name = "events"
    template_name = "countrycuzzins/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class VideoListView(ListView):
    model = Video
    context_object_name = "music_videos"
    template_name = "countrycuzzins/musicvideos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_video"] = get_object_or_404(Video, is_featured=True)
        return context

