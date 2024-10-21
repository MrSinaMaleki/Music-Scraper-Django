from django.contrib import admin
from apps.music.models import Music, Category

# Register your models here.
admin.site.register(Music)
admin.site.register(Category)
