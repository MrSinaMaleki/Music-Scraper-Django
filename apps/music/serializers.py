from rest_framework import serializers

from apps.music.models import Music, Category


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['title', 'singer', 'code', 'img', 'category', 'd_320p_link', 'd_128p_link']

class CategorySerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True)
    class Meta:
        model = Category
        fields = ['category_name', 'musics']
