from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from .models import Image

# Create your views here.

# Dont need this now
# Use detailView for the New feed ike in the flask app
class ImageList(ListView):
    model = Image
    context_object_name = 'image'
    template_name='countrycuzzins/index.html'

def index(request):
    context = {'img':Image
    }
    return render(request, "countrycuzzins/index.html", context)
