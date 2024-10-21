from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
from apps.music.models import Music

load_dotenv()

url = os.getenv('url')


def scrapper(site_url:str =url) -> list:
    if not site_url:
        raise ValueError('site_url cannot be empty')

    titles = list()
    singers = list()
    codes = list()
    images = list()

    res = requests.get(url)
    res.encoding = 'utf-8'
    bs = BeautifulSoup(res.text, 'html.parser')

    # Titles + Singers
    titles_singers =  bs.select('body > div.warpper > div > div.two-box-warpper > div > article:nth-child(3) > div:nth-child(6) > div > a > span')

    for item in [item.get_text().split('-') for item in titles_singers]:
        titles.append(item[1])
        singers.append(item[0])

    # Codes
    for item in bs.select('body > div.warpper > div > div.two-box-warpper > div > article:nth-child(3) > div:nth-child(6) > div > a'):
        codes.append(item['href'].split('/')[-2])

    # Img srcs
    for image in bs.select('body > div.warpper > div > div.two-box-warpper > div > article:nth-child(3) > div:nth-child(6) > div > a > img'):
        images.append(image['srcset'].split()[0])

    results = [{'title': title, 'singer':singer, 'code':code, 'image':image}
               for title, singer, code,image in zip(titles, singers, codes, images)
               ]


    return results


def uni_track(data:list):
    for track in data:
        track_obj = Music.objects.filter(code=track.get('code'))
        if track_obj:
            pass
        else:
            Music(title=track['title'], singer=track['singer'], code=track['code'], img=track['image']).save()
