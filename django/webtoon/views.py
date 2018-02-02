from django.http import HttpResponse
from django.shortcuts import render
from .models import Webtoon


def webtoon_list(request):
    webtoons = Webtoon.objects.all().order_by('-id')
    context = {
        'webtoons': webtoons,
    }
    return render(request, 'webtoon/index.html', context)


def webtoon_detail(request, pk):
    context = {
        'webtoon': Webtoon.objects.get(pk=pk),
    }
    return render(request, 'webtoon/webtoon_detail.html', context)
