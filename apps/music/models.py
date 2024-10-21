from django.db import models
from core.managers import LogicalMixin


class Category(LogicalMixin):
    category_name = models.CharField(max_length=255)


def get_default_category_name():
    return Category.objects.get_or_create(category_name='Not categorized')[0].id


class Music(LogicalMixin):
    title = models.CharField(max_length=255)
    singer = models.CharField(max_length=128)
    code = models.CharField(max_length=128, unique=True)
    img = models.ImageField(upload_to='music_image')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=get_default_category_name)

    def __str__(self):
        return f"{self.code}. {self.singer} --> {self.title}"
