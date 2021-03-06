from django.contrib import admin
from .models import Webtoon, Episode


@admin.register(Webtoon)
class WebtoonAdmin(admin.ModelAdmin):
    list_display = ('id', 'webtoon_id', 'title')


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'webtoon',
        'episode_id',
        'show_thumbnail',
        'title',
        'rating',
        'created_date'
    )
