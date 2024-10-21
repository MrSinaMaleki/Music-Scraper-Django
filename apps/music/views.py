from django.http import HttpResponse
from django.shortcuts import render
from core.utils import scrapper,uni_track

# Create your views here.

def index(request):
    uni_track(scrapper())
    return render(request, 'index.html', {'re': "hahah?"})
