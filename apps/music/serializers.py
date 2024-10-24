from rest_framework import serializers

from apps.music.models import Music


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['title', 'singer', 'code', 'img', 'category']
