from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    # re_path(r'(?:\(countrycuzzins/home|home\)/)?', views.index, name="home"),
    re_path(r"music-videos/$(?i)", views.music_videos, name="musicvideos"),
    re_path(r"events/$(?i)", views.EventList.as_view(), name="events"),
    path('video/<slug>/', views.VideoDetailView.as_view(), name="video")

]
