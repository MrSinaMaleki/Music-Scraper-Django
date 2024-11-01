from django.http import HttpResponse, Http404
from django.shortcuts import render
from core.utils import get_subjects,main_scrapper,uni_track
from .models import Music, Category
from rest_framework.views import APIView
from .serializers import MusicSerializer, CategorySerializer
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# Create your views here.

def index(request):
    # uni_track(scrapper())
    return render(request, 'index.html', {'re': "hahah?"})


@method_decorator(cache_page(1) , name='dispatch')
class ListAllTracks(APIView):
    """
    Getting the list of all the new tracks
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        uni_track(main_scrapper(get_subjects()))
        # print("In here ?!")
        tracks = Music.objects.all()
        serializer = MusicSerializer(tracks, many=True)
        return Response(serializer.data)


@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryListAllTracks(APIView):
    """
    Getting the list of all the tracks in a category.
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_objects(self, pk):
        try:
            # uni_track(main_scrapper(get_subjects()))
            # print("In here ?!")
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request,pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@method_decorator(cache_page(60 * 15), name='dispatch')
class TrackDetail(APIView):
    """
    Getting the details of the track.
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get_object(self, code):
        try:
            # uni_track(main_scrapper(get_subjects()))
            # print("In here ?!")
            return Music.objects.get(code=code)
        except Music.DoesNotExist:
            raise Http404

    def get(self, request, code):
        track = self.get_object(code)
        serializer = MusicSerializer(track)
        return Response(serializer.data)

