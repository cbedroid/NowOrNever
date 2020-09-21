from django.urls import path, re_path
from users import views as userviews
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    # re_path(r'(?:\(countrycuzzins/home|home\)/)?', views.index, name="home"),
    path("countrycuzzins/music-videos/", views.music_videos, name="musicvideos"),
    path("countrycuzzins/events/", views.EventList.as_view(), name="events"),
    path("countrycuzzins/contact_us/", userviews.contactUs, name="contact_us"),
]
