from django.http import HttpResponse, Http404
from django.shortcuts import render
from core.utils import scrapper,uni_track
from .models import Music
from rest_framework.views import APIView
from .serializers import MusicSerializer
from rest_framework.response import Response

# Create your views here.

def index(request):
    uni_track(scrapper())
    return render(request, 'index.html', {'re': "hahah?"})


class ListAllTracks(APIView):
    """
    Getting the list of all the new tracks
    """
    def get(self, request):
        tracks = Music.objects.all()
        serializer = MusicSerializer(tracks, many=True)
        return Response(serializer.data)


class TrackDetail(APIView):
    """
    Getting the details of the track.
    """
    def get_object(self, code):
        try:
            return Music.objects.get(code=code)
        except Music.DoesNotExist:
            raise Http404

    def get(self, request, code):
        track = self.get_object(code)
        serializer = MusicSerializer(track)
        return Response(serializer.data)

