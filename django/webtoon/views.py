from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Webtoon


def webtoon_list(request):
    webtoons = Webtoon.objects.all().order_by('-id')
    context = {
        'webtoons': webtoons,
    }
    return render(request, 'webtoon/webtoon_list.html', context)


def webtoon_detail(request, pk):
    context = {
        'webtoon': Webtoon.objects.get(pk=pk),
    }
    return render(request, 'webtoon/webtoon_detail.html', context)


def episode_get_list(request, pk):
    w1 = Webtoon.objects.get(pk=pk)
    w1.get_episode_list()
    # context = {
    #     'webtoon': w1,
    # }
    return redirect('webtoon-detail', pk=pk)
