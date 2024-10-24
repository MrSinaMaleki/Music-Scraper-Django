from django.urls import path
from .views import index, ListAllTracks, TrackDetail

urlpatterns = [
    path('',index, name='index'),
    path('all_songs/',ListAllTracks.as_view(), name='new_songs'),

    path('track_detail/<int:code>', TrackDetail.as_view(), name='track_detail' ),
]