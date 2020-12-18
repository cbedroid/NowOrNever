from django.urls import path, re_path
from . import views

app_name = "country_cuzzins"
urlpatterns = [
    path("", views.index, name="home"),
    re_path(r'^album/(?P<slug>.*)/$',
        views.AlbumDetailView.as_view(),
        name="album-detail"
    ),
    # NOTE: (THIS IS INTERNAL USE ONLY),**BUT** anonymous users can still
    #       crash the server by not adding "/"  to the end of post request.
    #       Fix this and make it unbreakable and protect it with csrf_token
    re_path(r"^song/playcount/(?P<pk>\d+)/$", 
        views.SongPlayCountView.as_view(), 
        name="song-playcount"
    ),
    re_path(r"music-videos/$(?i)", views.music_videos, name="musicvideos"),
    re_path(r"events/$(?i)", views.EventList.as_view(), name="events"),
    re_path(r'^video/(?P<slug>\w+)/$', views.VideoDetailView.as_view(), name="video")

]
