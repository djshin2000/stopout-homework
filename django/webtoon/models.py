import re
import os
import requests
from datetime import datetime
from django.db import models
from django.utils.html import format_html
from bs4 import BeautifulSoup
from config import settings


class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=15)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_episode_list(self):
        url = 'http://comic.naver.com/webtoon/list.nhn'
        params = {
            'titleId': self.webtoon_id,
            'page': 1,
        }
        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')

        tr_banner = soup.find('tr', class_='band_banner')
        if tr_banner:
            tr_banner.extract()

        tr_list = soup.select('table.viewList > tr')

        # media 폴더 및 webtoon app폴더가 없을 경우 폴더 생성
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        webtoon_dir = os.path.join(settings.MEDIA_ROOT, 'webtoon')
        os.makedirs(webtoon_dir, exist_ok=True)

        for tr in tr_list:
            onclick_text = tr.select_one('td:nth-of-type(2) > a').get('onclick')
            p = re.compile(r"\(.*?,.*?,.*?,.*?'(.*?)'.*?,.*?\)")
            episode_id = re.search(p, onclick_text).group(1)
            url_thumbnail = tr.select_one('td:nth-of-type(1) > a > img').get('src')
            title = tr.select_one('td:nth-of-type(2) > a').text
            rating = tr.select_one('td:nth-of-type(3) > div.rating_type > strong').text
            created_date_string = tr.select_one('td:nth-of-type(4)').text

            # string(2018.12.30)을 datetime format으로 변경
            created_date_object = datetime.strptime(created_date_string, '%Y.%m.%d')

            # 해당 webtoon의 폴더가 없을 경우 폴더 생성
            webtoon_id_dir = os.path.join(webtoon_dir, self.webtoon_id)
            os.makedirs(webtoon_id_dir, exist_ok=True)

            # thumbnail image를 저장하는 구문
            save_path = os.path.join(webtoon_id_dir, f'img{episode_id}.jpg')
            with open(save_path, 'wb') as f:
                f.write(requests.get(url_thumbnail).content)

            thumbnail_path = f'/media/webtoon/{self.webtoon_id}/img{episode_id}.jpg'

            Episode.objects.create(
                webtoon_id=self.pk,
                episode_id=episode_id,
                url_thumbnail=thumbnail_path,
                title=title,
                rating=rating,
                created_date=created_date_object,
            )


class Episode(models.Model):
    webtoon = models.ForeignKey('Webtoon', on_delete=models.CASCADE)
    episode_id = models.CharField(max_length=10)
    url_thumbnail = models.CharField(max_length=255, blank=True, default=None, null=True)
    title = models.CharField(max_length=200)
    rating = models.CharField(max_length=5)
    created_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    def show_thumbnail(self):
        return format_html(
            f'<img src="" width="71" height="41" />'
        )
