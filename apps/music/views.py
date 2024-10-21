from django.http import HttpResponse
from django.shortcuts import render
from core.utils import scrapper

# Create your views here.

def index(request):
    return render(request, 'index.html', {'re': scrapper()})
