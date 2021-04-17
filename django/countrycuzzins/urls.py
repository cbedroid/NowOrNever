from django.urls import re_path
from . import views

app_name = "country_cuzzins"
urlpatterns = [
    re_path(r'^album/(?P<slug>.*)/$', views.AlbumDetailView.as_view(), name="album-detail"),
    re_path(r"^song/playcount/(?P<pk>\d+)/$", views.SongPlayCountView.as_view(), name="song-playcount"),
    re_path(r"^music/videos/$(?i)", views.VideoListView.as_view(), name="musicvideos"),
    re_path(r'^music/video/(?P<id>\d+)/$', views.VideoListView.as_view(), name="musicvideo-rate"),
    re_path(r"events/$(?i)", views.EventList.as_view(), name="events"),
    re_path(r"", views.HomeView.as_view(), name="home"),
]
