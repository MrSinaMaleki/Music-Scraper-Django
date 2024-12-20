from django.db import models
from core.managers import LogicalMixin


class Category(LogicalMixin):
    category_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


def get_default_category_name():
    return Category.objects.get_or_create(category_name='Not categorized')[0].id


class Music(LogicalMixin):
    title = models.CharField(max_length=255)
    singer = models.CharField(max_length=128)
    code = models.CharField(max_length=128, unique=True)
    img = models.ImageField(upload_to='music_image')
    category = models.ForeignKey(Category,related_query_name="musics",related_name='musics', on_delete=models.CASCADE, default=get_default_category_name)
    d_320p_link = models.CharField(max_length=255, null=True, blank=True)
    d_128p_link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'Musics'
        ordering = ('created_at',)
        indexes = [models.Index(fields=['code'])]

    def __str__(self):
        return f"{self.code}. {self.singer} --> {self.title}"
