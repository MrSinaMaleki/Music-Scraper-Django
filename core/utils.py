from tkinter import image_names
from tkinter.font import names

from bs4 import BeautifulSoup
import requests
import os

from django.core.files.base import ContentFile
from dotenv import load_dotenv
from apps.music.models import Music
from PIL import Image
from io import BytesIO



load_dotenv()

url = os.getenv('url')


import requests
from bs4 import BeautifulSoup

url = "https://musicdel.ir"



def get_subjects(url_address:str = url) -> list:
    if not url_address:
        raise ValueError("url cannot be empty")

    categories =[]
    category_urls = []

    res = requests.get(url_address)
    res.encoding = "utf-8"
    bs = BeautifulSoup(res.text, "html.parser")

    a_tags = bs.select('.top > ul > li > a')
    for a_tag in a_tags:
        category_urls.append(a_tag.get('href'))
        categories.append((a_tag.get('title')).replace("دانلود ", "").replace("آهنگ ", "").replace("های", ""))

    results = [{'category_title': category, "category_url": category_url}
               for category, category_url in zip(categories, category_urls)]


    return results


def main_scrapper(categories_links):
    del categories_links[0]
    del categories_links[2]
    del categories_links[2]
    titles_list = list()
    singers_list = list()
    codes = list()
    images = list()
    d320p_tags = list()
    d128p_tags = list()
    n_of_tracks = list()
    raw_category_list = list()


    for link in categories_links:
        raw_category_list.append(link.get('category_title'))

        res = requests.get(link.get('category_url'))
        res.encoding = 'utf-8'
        bs = BeautifulSoup(res.text, "html.parser")

        d320p_d128p_tags = bs.select('article > div > div> .downloads2 > .downloads > a')
        index = 0
        while index < len(d320p_d128p_tags):
            d320p_tags.append(d320p_d128p_tags[index].get('href'))
            index += 1
            d128p_tags.append(d320p_d128p_tags[index].get('href'))
            index += 1



        image_tags = bs.select('body > div.warpper > div > div.two-box-warpper > div > article:nth-child(5) > div > div > a > img')
        for image_tag in image_tags:
            images.append(image_tag.get('src'))



        link_tags = bs.select('body > div.warpper > div > div.two-box-warpper > div > article:nth-child(5) > div > div > a')
        for link_tag in link_tags:
            codes.append((link_tag.get('href').split("/"))[4])



        title_span_tags = bs.select('div > div > a > span')
        title_span_tags_mod_text = [(title.get_text()).replace("دانلود ", "").replace("آهنگ ", "") for title in title_span_tags]

        for title_singer in title_span_tags_mod_text:
            t_s = title_singer.split("از")
            titles_list.append(t_s[0])
            singers_list.append(t_s[1] if len(t_s) >= 2 else "No Singer")

        n_of_tracks.append(int(len(link_tags)))

    categories = [item for item, number in zip(raw_category_list, n_of_tracks) for _ in range(number)]

    results = [{'title': title, 'singer': singer, 'code': code, 'image': image, "320p_download_link": d320, "128p_download_link": d128}
               for title, singer, code, image, d320, d128 in zip(titles_list, singers_list, codes, images, d320p_tags, d128p_tags )
               ]

    # data test debugs:
    # print("d320p_tags: ", d320p_tags, "len: ", len(d320p_tags), sep="\n", end="\n\n")
    # print("d120p_tags: ", d128p_tags, "len: ", len(d128p_tags), sep="\n", end="\n\n")
    # print("codes: ", codes, "len: ", len(codes), sep="\n", end="\n\n")
    # print("image scr: : ", images, "len: ", len(images), sep="\n", end="\n\n")
    # print("titles: ", titles_list, "len: ", len(titles_list), sep="\n", end="\n\n")
    # print("singers: ", singers_list, "len: ", len(singers_list), sep="\n", end="\n\n")

    return results





def uni_track(data:list):
    for track in data:
        track_obj = Music.objects.filter(code=track.get('code'))
        if track_obj:
            pass
        else:
            ins = Music(title=track['title'], singer=track['singer'], code=track['code'], d_320p_link=track['320p_download_link'], d_128p_link=track['128p_download_link'])
            image_file_from_url(instance=ins, url_address=track['image'])
            ins.save()


def image_file_from_url(instance:Music,url_address:str ):
    try:
        response = requests.get(url_address)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))

        img_io = BytesIO()
        img_format = img.format if img.format else 'JPEG'
        img.save(img_io, format=img_format)

        img_content = ContentFile(img_io.getvalue(), name=f'CoverImage_{instance.code}.{img_format.lower()}')

        instance.img.save(img_content.name, img_content, save=True)
        instance.save()


    except requests.exceptions.RequestException as e:
        print(f'Error Downloading the images: {e}')

    except Exception as e:
        print(f'Error Saving the images: {e}')
