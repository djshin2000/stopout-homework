from bs4 import BeautifulSoup
import requests
import os
import re

PATH_MODULE = os.path.abspath(__file__)
ROOT_DIR = os.path.dirname(PATH_MODULE)
file_path = os.path.join(ROOT_DIR, 'webtoon_episode.html')


class EpisodeData:

    def __init__(self, episode_id, url_thumbnail, title, rating, created_date):
        self.episode_id = episode_id
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    def __str__(self):
        return f'{self.episode_id}: {self.title}'


def get_episode_list(webtoon_id, page):
    url = 'http://comic.naver.com/webtoon/list.nhn'
    params = {
        'titleId': webtoon_id,
        'page': page,
    }
    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')

    # file에서 읽어오는 구문
    # with open(file_path, 'rt') as f:
    #     source = f.read()
    # soup = BeautifulSoup(source, 'lxml')

    # table 태그안에 배너 tr이 있는 경우 삭제하는 구문
    tr_banner = soup.find('tr', class_='band_banner')
    if tr_banner:
        tr_banner.extract()

    tr_list = soup.select('table.viewList > tr')

    episode_list = []
    for tr in tr_list:
        onclick_text = tr.select_one('td:nth-of-type(2) > a').get('onclick')
        p = re.compile(r"\(.*?,.*?,.*?,.*?'(.*?)'.*?,.*?\)")
        episode_id = re.search(p, onclick_text).group(1)
        url_thumbnail = tr.select_one('td:nth-of-type(1) > a > img').get('src')
        title = tr.select_one('td:nth-of-type(2) > a').text
        rating = tr.select_one('td:nth-of-type(3) > div.rating_type > strong').text
        created_date = tr.select_one('td:nth-of-type(4)').text

        episode_data = EpisodeData(
            episode_id=episode_id,
            url_thumbnail=url_thumbnail,
            title=title,
            rating=rating,
            created_date=created_date
        )
        episode_list.append(episode_data)
    return episode_list


if __name__ == '__main__':
    results = get_episode_list(695321, 2)
    for result in results:
        print('{} | {} | {} | {} | {}'.format(
            result.episode_id,
            result.url_thumbnail,
            result.title,
            result.rating,
            result.created_date
        ))
