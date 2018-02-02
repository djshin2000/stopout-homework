from django.http import HttpResponse
from django.shortcuts import render
from .models import Webtoon, Episode


def webtoon_list(request):
    webtoons = Webtoon.objects.all().order_by('-id')
    context = {
        'webtoons': webtoons,
    }

    return render(request, 'webtoon/index.html', context)


def webtoon_detail(request, pk):
    episodes = Episode.objects.filter(webtoon=pk)
    context = {
        'episodes': episodes,
    }
    return render(request, 'webtoon/webtoon_detail.html', context)
