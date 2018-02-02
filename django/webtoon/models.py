import re
import requests
from bs4 import BeautifulSoup
from django.db import models
from django.utils.html import format_html


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

        for tr in tr_list:
            onclick_text = tr.select_one('td:nth-of-type(2) > a').get('onclick')
            p = re.compile(r"\(.*?,.*?,.*?,.*?'(.*?)'.*?,.*?\)")
            episode_id = re.search(p, onclick_text).group(1)
            url_thumbnail = tr.select_one('td:nth-of-type(1) > a > img').get('src')
            title = tr.select_one('td:nth-of-type(2) > a').text
            rating = tr.select_one('td:nth-of-type(3) > div.rating_type > strong').text
            created_date = tr.select_one('td:nth-of-type(4)').text

            Episode.objects.create(
                webtoon=self.webtoon_id,
                episode_id=episode_id,
                url_thumbnail=url_thumbnail,
                title=title,
                rating=rating,
                created_date=created_date,
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
            f'<img src="{self.url_thumbnail}" width="71" height="41" />'
        )
