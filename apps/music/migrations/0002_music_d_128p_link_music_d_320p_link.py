# Generated by Django 5.1.2 on 2024-10-31 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='d_128p_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='music',
            name='d_320p_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
