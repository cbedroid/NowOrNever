from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Image, Article, Video, SocialMedia, Event
from .music_models import Album, Song

# Create your views here.


class EventList(ListView):
    model = Event
    context_object_name = "events"
    template_name = "countrycuzzins/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def index(request):
    context = {
        "articles": Article.objects.all(),
        "albums": Album.objects.filter(name="Country Cuzzins"),
        "images": Image.objects.all(),
        "music_videos": Video.objects.filter(is_music=True),
        "social_media": SocialMedia,
    }
    return render(request, "countrycuzzins/index.html", context)


@never_cache
def music_videos(request):
    context = {"music_videos": list(Video.objects.all())}
    return render(request, "countrycuzzins/musicvideos.html", context)
