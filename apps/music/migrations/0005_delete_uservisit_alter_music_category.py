# Generated by Django 5.1.2 on 2024-10-24 20:20

import apps.music.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_uservisit_delete_dailyurlvisit_delete_dailyvisit'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserVisit',
        ),
        migrations.AlterField(
            model_name='music',
            name='category',
            field=models.ForeignKey(default=apps.music.models.get_default_category_name, on_delete=django.db.models.deletion.CASCADE, related_name='musics', related_query_name='musics', to='music.category'),
        ),
    ]