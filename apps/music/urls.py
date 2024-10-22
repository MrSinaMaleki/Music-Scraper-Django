from django.urls import path
from .views import index, ListAllTracks

urlpatterns = [
    path('',index, name='index'),
    path('new_songs/',ListAllTracks.as_view(), name='new_songs'),
]