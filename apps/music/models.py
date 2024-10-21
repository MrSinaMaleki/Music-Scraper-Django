from django.db import models
from core.managers import LogicalMixin


class Music(LogicalMixin):
    title = models.CharField(max_length=255)
    singer = models.CharField(max_length=128)
    code = models.CharField(max_length=128, unique=True)
    img = models.ImageField(upload_to='music')

    def __str__(self):
        return f"{self.code}. {self.singer} --> {self.title}"
