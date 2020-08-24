from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView,DetailView
from .models import Image, Article, Video,SocialMedia
from .music_models import Album

# Create your views here.

# Dont need this now
# Use detailView for the New feed ike in the flask app
class ArticleDetailView(DetailView):
    model = Article
    template_name='countrycuzzins/article.html'

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['now'] = timezone.now()
      return context
    
class ImageList(DetailView):
    model = Image
    context_object_name = 'image'
    template_name='countrycuzzins/index.html'

class AlbumList(ListView):
    model = Album
    context_object_name = 'albums'
    #template_name='countrycuzzins/snippets/_music_player.html'
    # new Msic player testing
    template_name='countrycuzzins/snippets/testing_music_player.html'

    def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['now'] = timezone.now()
          return context


def index(request):
    context = {'articles':Article.objects.all(),
    'albums':Album.objects.filter(name="Country Cuzzins"), 
    'images':Image.objects.all(),
    'music_videos': Video.objects.filter(is_music=True),
    'social_media': SocialMedia,

    }
    return render(request, "countrycuzzins/index.html", context)

def accountLogin(request):
  context = {}
  return render(request,"countrycuzzins/snippets/account/login.html",context)



#########################################################
#           *************************                   #
#           ****  TESTER VIEWS   ****                   #
#           *************************                   #
#########################################################

from .models import Song

def test_music_player(request):
  songs = Song.objects.all()
  context = {'music': songs}
  return render(request,"countrycuzzins/testing/_music_player.html",context)

def test_html(request):
  #testing html 
  context = {}
  return render(request,"countrycuzzins/testing/_testing.html",context)


