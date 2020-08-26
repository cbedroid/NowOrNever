from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from .models import Image, Article, Video,SocialMedia
from .music_models import Album
from .forms import RegistrationForm

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


def accountSignup(request):
  context = {}
  form = RegistrationForm(request.POST or None)
  if request.method == "POST":
    if form.is_valid():
      user = form.save()
      print('USER',user)
      login(request,user)
      messages.success(request, '% Welcome %s'%user.username)
      return reverse('index')
      return HttpResponseRedirect(reverse('index'))
  context['form']=form
  return render(request,'countrycuzzins/snippets/account/signup.html',context)



def accountLogin(request):
  if request.method == 'POST':
      form = AuthenticationForm(request=request, data=request.POST)
      if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
          login(request, user)
          messages.info(request, f"You are now logged in as {username}")
          return HttpResponseRedirect(reverse('index'))
        else:
          messages.error(request, "Invalid username or password.")
      else:
        messages.error(request, "Invalid username or password.")
  form = AuthenticationForm()
  return render(request,"countrycuzzins/snippets/account/login.html",
                  context={"form":form})

@never_cache
def accountLogin2(request):
  print(request.POST)

  form = AuthenticationForm
  username = request.POST.get('username')
  password = request.POST.get('password')
  user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)
    return HttpResponseRedirect(reverse('index'))
  else:
    form = User
    return render(request,"countrycuzzins/snippets/account/login.html")
  return render(request,"countrycuzzins/snippets/account/login.html")

def accountLogout(request):
  logout(request)
  messages.info(request, "Logged out successfully!")
  return HttpResponseRedirect(reverse('index'))

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


