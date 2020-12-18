from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from .models import Image, Article, Video, SocialMedia, Event
from .music_models import Album, Song

# Create your views here.

def index(request):
    context = {
        #"album": get_object_or_404(Album,is_featured=True),
        "album": Album.objects.all()[0],
        "images": Image.objects.all(),
        "music_videos": Video.objects.all(),
        "social_media": SocialMedia,
        "test_image": Image.objects.last(),
    }
    return render(request, "countrycuzzins/index.html", context)


# class AlbumListView(ListView):
#     """ Get all song data from album"""
#     """
#       NOTE: Add this to change the way songs are passed to musicplayer
#      - Good: My first instinct was to request each song one by one and use
#              "SongView" method to collect each song. Doing this will be
#              problematic and will put a lot of stress on the server each time
#              a user listen to a song or view album.

#     -  Better: Instead of collecting each song one by one, I used the database 
#                relationship method and cache approach to collect all song
#                meta's data from album. Using this approach we will make only
#                one request to the server and use cached (client-side cache) 
#                the store the data. This is will speed optimize and cause less
#                stress one the server.
#     """
#     model = Album
#     template_name = "countrycuzzins/album-detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["songs"] = self.object.songs.get_queryset()
#         return context



class AlbumDetailView(DetailView):
    model = Album
    template_name = "countrycuzzins/album-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["songs"] = self.object.songs.get_queryset()
        return context


class SongPlayCountView(View):
    model = Song
    response = {'success':False,"data":{}}


    def post(self,*args,**kwargs):
        song_id = self.request.POST.get('pk') or kwargs.get('pk')
        print('SONG_ID',song_id)
        album_songs = Song.objects.all()
        song = album_songs.filter(pk=song_id)
        if song.exists() and album_songs.exists(): 
            album_song_views = [] 
            if song:
                song = song.first()
                song.played_count +=1
                self.response.update(dict(data=
                    dict(
                        song = song.name,
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



@never_cache
def music_videos(request):
    context = {"music_videos": list(Video.objects.all())}
    return render(request, "countrycuzzins/musicvideos.html", context)


class VideoDetailView(DetailView):
    model = Video
    template_name = "countrycuzzins/test_video.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add all other videos ( non featured videos)
        context['videos'] = Video.objects.all()
        return context
